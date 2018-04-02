"""
The Game World controller that contains the current state and can render the
world
"""

from __future__ import absolute_import, print_function, division

from PIL import ImageDraw
import random
import os
import json
import shutil

class CageWorld(object):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self, config):
        self.width = config.getint('world', 'width', fallback=480)
        self.height = config.getint('world', 'height', fallback=480)
        self.fps = config.getint('world', 'fps', fallback=10)
        self.gameseconds = config.getint('world', 'duration', fallback=10)
        self.gametick = 0
        self.gameticks = self.fps * self.gameseconds
        self.background = (0, 0, 0, 255)
        self.num_fighters = config.getint('world', 'num_fighters', fallback=2)
        self.fighter_controllers = [
            config.get(
                'fighter_%s' % (fighterid,), 'docker',
                fallback='cagefighterbasic:latest',
            ) for fighterid in range(self.num_fighters)
        ]
        self.fighters = []
    @classmethod
    def load(cls, config):
        """
        Load the appropriate gameworld based on the config
        """
        worldkind = config.get('world', 'kind', fallback='lightning')
        worlds = cls.get_world_lookup()
        return worlds[worldkind](config)
    def save_world_state(self, basedir, gametick):
        """
        serialize game state to file
        """
        subdir = os.path.join(basedir, gametick)
        if not os.path.isdir(subdir):
            os.makedirs(subdir)
        worldfile = os.path.join(subdir, 'world.json')
        with open(worldfile, 'w') as fobj:
            json.dump(self.save_world_to_json(), fobj)
    def save_fighters(self, basedir):
        """
        serialize information for fighters to file
        """
        for fighterid in range(self.num_fighters):
            self.save_fighter(basedir, fighterid)
    def save_fighter(self, basedir, fighterid):
        """
        serialize information for a fighter to file
        """
        subdir = os.path.join(basedir, 'fighter_%s' % (
            fighterid,
        ))
        if os.path.isdir(subdir):
            shutil.rmtree(subdir)
        os.mkdir(subdir)
        worldfile = os.path.join(subdir, 'world.json')
        with open(worldfile, 'w') as fobj:
            json.dump(
                self.save_fighter_world_to_json(
                    fighterid,
                ),
                fobj,
            )
    def save_world_to_json(self):
        """
        serialize game state
        """
        result = {
            'num_fighters': self.num_fighters,
        }
        for fighter_id, fighter in enumerate(self.fighters):
            result['fighter_%s' % (fighter_id,)] = fighter.save()
        return result
    def save_fighter_world_to_json(self, fighterid):
        """
        serialize single player game view
        """
        return self.fighters[fighterid].save_view()
    def load_world_state(self, basedir, gametick):
        """
        deserialize game state from file
        """
        worldfile = os.path.join(basedir, gametick, 'world.json')
        with open(worldfile) as fobj:
            jsonobj = json.load(fobj)
        self.load_world_from_json(jsonobj)
    def load_world_from_json(self, jsonobj):
        """
        deserialize game state
        """
        self.fighters = []
        self.num_fighters = jsonobj['num_fighters']
        for fighterid in range(self.num_fighters):
            fighter = self.get_fighter(fighterid)
            fighter.load(jsonobj['fighter_%s' % (fighterid,)])
            self.fighters.append(fighter)
    def run_fighters(self, basedir):
        """
        Simulate running the fighters in process for speed.
        """
        for fighter_id, controller in enumerate(self.fighter_controllers):
            fighterdir = os.path.join(basedir, 'fighter_%s' % (fighter_id,))
            modname = controller.split(':', 1)[0]
            modobj = __import__('%s.main' % (modname,))
            modobj.main.main(fighterdir)
    def save_runsheet(self, fobj):
        """
        Produce the docker run bash script
        """
        commands = self.get_commands()
        print("""\
#!/bin/bash

BASEDIR=$(dirname $(readlink -f "$0"))
. ${BASEDIR}/env.sh
%s
""" % (
    '\n'.join(commands),
), file=fobj)
    def get_commands(self):
        """
        Return the sequence of controller, fighters for each game step before
        the final render step.
        """
        commands = ['if [ ! -e "%s" ] ; then mkdir --parents "%s" ; fi' % (
            dirname,
            dirname,
        ) for dirname in (
            '${BASEDIR}/var/out/fighter_%s' % (fighterid,) for
                fighterid, _ in enumerate(self.fighter_controllers)
        )]
        main_out = {
            key: key for key in (
                '/var/out/fighter_%s/world.json' % (fighterid,)
                for fighterid, _ in enumerate(self.fighter_controllers)
            )
        }
        commands.append(
            self.get_command(
                'cagefightsrc:latest', {}, main_out,
                'python /src/maincagefight.py --start',
            )
        )
        for gametick in range(self.gameticks):
            for fighterid, dockername in enumerate(self.fighter_controllers):
                fighter_in = {
                    '/var/out/fighter_%s/world.json' % (fighterid,):
                        '/var/out/world.json'
                }
                commands.append(
                    self.get_command(
                        dockername, fighter_in, {},
                        '/plan.sh'
                    )
                )
            commands.append(
                self.get_command(
                    'cagefightsrc:latest', {}, {},
                    'python /src/maincagefight.py --step %s' % (gametick,),
                )
            )
        commands.append(
            self.get_command(
                'cagefightsrc:latest', {}, {},
                'python /src/maincagefight.py --render',
            )
        )
        return commands
    def get_command(self, dockertag, files_in, files_out, cmd):
        """
        Return the appropriate command to run the docker step
        """
        return """\
CONTID=$(docker create -t "%(dockertag)s" sleep 600)
docker start "${CONTID}"
%(file_copy_in)s
docker exec "${CONTID}" %(cmd)s
%(file_copy_out)s
docker stop "${CONTID}"
docker rm "${CONTID}"
""" % {
    'dockertag': dockertag,
    'cmd': cmd,
    'file_copy_in': '\n'.join(
        'docker cp "$(os_path "${BASEDIR}%s")" "${CONTID}:%s"' % (
            key, val
        ) for key, val in files_in.items()
    ),
    'file_copy_out': '\n'.join(
        'docker cp "${CONTID}:%s" "$(os_path "${BASEDIR}%s")"' % (
            key, val
        ) for key, val in files_out.items()
    ),
}
    @classmethod
    def get_world_lookup(cls):
        """
        Create a kind: class lookup of world kinds
        """
        worldkinds = cls.get_world_kinds()
        return {
            worldkind.kind(): worldkind for worldkind in worldkinds
        }
    @classmethod
    def get_world_kinds(cls):
        """
        A list of possible world kinds
        """
        from .lightningworld import LightningWorld
        return [
            LightningWorld,
        ]
    @classmethod
    def kind(cls):
        """
        Overridden to provide a world kind key
        """
        raise NotImplementedError('Override to provide a kind')
    def start(self):
        """
        Called prior to the first render to prepare the starting state.
        """
        self.fighters = [
            self.get_fighter(num) for num in range(self.num_fighters)
        ]
        for fighter in self.fighters:
            fighter.start()
    def next(self, basedir, gametick):
        """
        Progress the game state to the next tick.
        """
        self.gametick = gametick
        for fighter_id, fighter in enumerate(self.fighters):
            filepath = os.path.join(
                basedir, 'fighter_%s' % (fighter_id,), 'out.json'
            )
            fighter.next(filepath)
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        for fighter in self.fighters:
            fighter.render(im)
    def get_fighter(self, fighterid):
        """
        Override to construct the appropriate fighter
        """
        raise NotImplementedError('Override to prepare fighter')
    @staticmethod
    def draw_ball(im, x, y, size, colour):
        """
        Draw a lightning ball
        """
        draw = ImageDraw.Draw(im)
        x0 = x
        y0 = y
        for _ in range(5):
            x1 = x + random.randrange(0, size) - (size / 2)
            y1 = y + random.randrange(0, size) - (size / 2)
            draw.line((x0, y0, x1, y1), fill=colour)
    @staticmethod
    def collision(x1, y1, x2, y2, size):
        """
        Check for a collision between two coordinates and a proximity
        """
        return (
            (x1 - size <= x2 <= x1 + size)
            and
            (y1 - size <= y2 <= y1 + size)
        )

