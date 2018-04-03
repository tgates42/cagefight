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
        self.fps = config.getint('world', 'fps', fallback=25)
        self.gameseconds = config.getint('world', 'duration', fallback=30)
        self.gametick = 0
        self.gameticks = self.fps * self.gameseconds
        self.background = (0, 0, 0, 255)
        self.num_fighters = config.getint('world', 'num_fighters', fallback=5)
        self.fighter_controllers = [
            config.get(
                'fighter_%s' % (fighterid,), 'docker',
                fallback='cagefighterbasic:latest',
            ) for fighterid in range(self.num_fighters)
        ]
        self.fighters = []
        self.projectiles = []
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
            'num_projectiles': len(self.projectiles),
        }
        for fighter_id, fighter in enumerate(self.fighters):
            result['fighter_%s' % (fighter_id,)] = fighter.save()
        for projectile_id, projectile in enumerate(self.projectiles):
            result['projectile_%s' % (projectile_id,)] = projectile.save()
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
        num_projectiles = jsonobj['num_projectiles']
        self.projectiles = []
        for projectileid in range(num_projectiles):
            projectile = self.get_projectile()
            projectile.load(jsonobj['projectile_%s' % (projectileid,)])
            self.projectiles.append(projectile)
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
        ) for dirname in ([
            '${BASEDIR}/var/out/fighter_%s' % (fighterid,) for
                fighterid, _ in enumerate(self.fighter_controllers)
        ] + [
            '${BASEDIR}/var/out/step_%s' % (gametick,)
                for gametick in range(self.gameticks)
        ] + [
            '${BASEDIR}/var/out/start',
        ])]
        main_in = {
            key: key for key in (
                '/var/out/fighter_%s/out.json' % (fighterid,)
                for fighterid, _ in enumerate(self.fighter_controllers)
            )
        }
        main_out = {
            key: key for key in (
                '/var/out/fighter_%s/world.json' % (fighterid,)
                for fighterid, _ in enumerate(self.fighter_controllers)
            )
        }
        fighter_dirs = [
            '/var/out/fighter_%s' % (fighterid,)
                for fighterid, _ in enumerate(self.fighter_controllers)
        ]
        step_dirs = [
            '/var/out/start',
        ]
        start_out = dict(main_out)
        worldstate = {
            '/var/out/start/world.json': '/var/out/start/world.json',
        }
        render_in = {}
        start_out.update(worldstate)
        render_in.update(worldstate)
        last_step = 'start'
        commands.append(
            self.get_command(
                'cagefightsrc:latest', {}, start_out,
                'python /src/maincagefight.py --start',
                [],
            )
        )
        for gametick in range(self.gameticks):
            for fighterid, dockername in enumerate(self.fighter_controllers):
                fighter_in = {
                    '/var/out/fighter_%s/world.json' % (fighterid,):
                        '/var/out/world.json'
                }
                fighter_out = {
                    '/var/out/out.json':
                        '/var/out/fighter_%s/out.json' % (fighterid,)
                }
                commands.append(
                    self.get_command(
                        dockername, fighter_in, fighter_out,
                        '/plan.sh', [],
                    )
                )
            worldstate = {
                '/var/out/%s/world.json' % (last_step,):
                    '/var/out/%s/world.json' % (last_step,),
            }
            main_dirs = fighter_dirs + ['/var/out/%s' % (last_step,)]
            step_in = dict(main_in)
            step_in.update(worldstate)
            render_in.update(worldstate)
            last_step = 'step_%s' % (gametick,)
            step_out = dict(main_out)
            step_out.update({
                '/var/out/%s/world.json' % (last_step,):
                    '/var/out/%s/world.json' % (last_step,),
            })
            step_dirs.append('/var/out/%s' % (last_step,))
            commands.append(
                self.get_command(
                    'cagefightsrc:latest', step_in, step_out,
                    'python /src/maincagefight.py --step %s' % (gametick,),
                    main_dirs,
                )
            )
        commands.append(
            self.get_command(
                'cagefightsrc:latest', render_in, {
                    '/var/out/output.mp4': '/var/out/output.mp4',
                },
                'python /src/maincagefight.py --render',
                step_dirs,
            )
        )
        return commands
    def get_command(self, dockertag, files_in, files_out, cmd, mkdirs):
        """
        Return the appropriate command to run the docker step
        """
        return """\
CONTID=$(docker create -t "%(dockertag)s" sleep 600)
docker start "${CONTID}"
%(mkdir_cmd)s
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
    'mkdir_cmd': '\n'.join(
        'docker exec "${CONTID}" mkdir -p %s' % (dirname,)
            for dirname in mkdirs
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
        for projectile in self.projectiles:
            projectile.next()
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        for fighter in self.fighters:
            fighter.render(im)
        for projectile in self.projectiles:
            projectile.render(im)
    def get_fighter(self, fighterid):
        """
        Override to construct the appropriate fighter
        """
        raise NotImplementedError('Override to prepare fighter')
    def get_projectile(self):
        """
        Override to construct the appropriate projectile
        """
        raise NotImplementedError('Override to prepare projectile')
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
    def add_projectile(self, projectile):
        """
        Add a projectile to the world
        """
        self.projectiles.append(projectile)

