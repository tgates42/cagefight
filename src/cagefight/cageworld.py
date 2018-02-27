"""
The Game World controller that contains the current state and can render the
world
"""

from __future__ import absolute_import, print_function, division

from PIL import ImageDraw

class CageWorld(object):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self):
        self.width = 480
        self.height = 480
        self.fps = 25
        self.gameseconds = 60
        self.gametick = 0
        self.gameticks = self.fps * self.gameseconds
        self.background = (0, 0, 0, 255)
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
        draw = ImageDraw.Draw(im)
        x0 = self.gametick
        x1 = self.gametick
        y0 = 0
        y1 = self.height
        colour = (0, 255, 255, 255)
        draw.line((x0, y0, x1, y1), fill=colour)
        return im

