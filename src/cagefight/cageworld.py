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
    @classmethod
    def load(cls, config):
        """
        Load the appropriate gameworld based on the config
        """
        worldkind = config.get('world', 'kind', fallback='lightning')
        worlds = cls.get_world_lookup()
        return worlds[worldkind](config)
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
        pass
    def next(self):
        """
        Progress the game state to the next tick.
        """
        self.gametick += 1
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        raise NotImplementedError('Override to draw display')
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
