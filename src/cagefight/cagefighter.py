"""
The base fighter implementation
"""

from __future__ import absolute_import, print_function, division

class CageFighter(object):
    """
    Base fighter implementation
    """
    colours = [
        (55, 255, 255, 255),
        (255, 55, 255, 255),
        (255, 255, 55, 255),
        (55, 55, 255, 255),
        (255, 55, 55, 255),
        (55, 255, 55, 255),
    ]
    def __init__(self, world, fighterid):
        self.world = world
        self.fighterid = fighterid
    def start(self):
        """
        Called prior to the first render to prepare the starting state.
        """
        pass
    def next(self):
        """
        Progress the game state to the next tick.
        """
        pass
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        raise NotImplementedError('Override to draw fighter')
    def get_instructions(self):
        """
        Pas the world
        """
        # TODO: call out to docker
        return {}
