"""
The Game World controller that contains the current state and can render the
world
"""

from __future__ import absolute_import, print_function, division

from PIL import ImageDraw
import random

class CageWorld(object):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self, config):
        self.width = config.getint('world', 'width', fallback=480)
        self.height = config.getint('world', 'height', fallback=480)
        self.fps = config.getint('world', 'fps', fallback=25)
        self.gameseconds = config.getint('world', 'duration', fallback=60)
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
""" % ('\n'.join(commands),), file=fobj)
    def get_commands(self):
        """
        Return the sequence of controller, fighters for each game step before
        the final render step.
        """
        commands = []
        commands.append(
            self.get_command(
                'cagefightsrc:latest', '/var/out',
                'python /src/maincagefight.py --start',
            )
        )
        for gametick in range(self.gameticks):
            for fighterid, dockername in enumerate(self.fighter_controllers):
                commands.append(
                    self.get_command(
                        dockername, '/var/out/fighter_%s' % (fighterid,),
                        ''
                    )
                )
            commands.append(
                self.get_command(
                    'cagefightsrc:latest', '/var/out',
                    'python /src/maincagefight.py --step %s' % (gametick,),
                )
            )
        commands.append(
            self.get_command(
                'cagefightsrc:latest', '/var/out',
                'python /src/maincagefight.py --render',
            )
        )
        return commands
    def get_command(self, dockertag, subdir, cmd):
        """
        Return the appropriate command to run the docker step
        """
        return """\
docker run -v "$(os_path ${BASEDIR}%s)":/var/out -t %s %s
""" % (subdir, dockertag, cmd)
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
    def next(self):
        """
        Progress the game state to the next tick.
        """
        self.gametick += 1
        for fighter in self.fighters:
            fighter.next()
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

