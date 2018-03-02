"""
The base fighter implementation
"""

from __future__ import absolute_import, print_function, division

import os
import json

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
    def next(self, filepath):
        """
        Progress the game state to the next tick.
        """
        pass
    def save(self):
        """
        Override to save details of current fighter with total knowledge
        """
        raise NotImplementedError('Override to save fighter')
    def save_view(self):
        """
        Override to save details of current fighter with fighter knowledge,
        default implementation assumes total knowledge
        """
        return self.save()
    def load(self, jsonobj):
        """
        Override to load details of current fighter
        """
        raise NotImplementedError('Override to load fighter')
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        raise NotImplementedError('Override to draw fighter')
    def get_instructions(self, filepath):
        """
        Load instructions from the filepath
        """
        if not os.path.isfile(filepath):
            return {}
        with open(filepath) as fobj:
            return json.load(fobj)
