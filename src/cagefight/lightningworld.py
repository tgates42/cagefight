"""
A very simple game involving lightning spheres that can attack each other
"""

from __future__ import absolute_import, print_function, division

from cagefight.cageworld import CageWorld
import random

class LightningWorld(CageWorld):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self, config):
        super(LightningWorld, self).__init__(config)
        self.pos_x = 0
        self.pos_y = 0
    def start(self):
        """
        Initial game state
        """
        super(LightningWorld, self).start()
        self.pos_x = random.randrange(self.width)
        self.pos_y = random.randrange(self.height)
    def next(self):
        """
        Progress game state
        """
        super(LightningWorld, self).start()
        self.pos_x += random.randrange(3) - 1
        self.pos_y += random.randrange(3) - 1
    @classmethod
    def kind(cls):
        """
        Overridden to provide a world kind key
        """
        return 'lightning'
    def render(self, im):
        """
        Draw the current player positions
        """
        self.draw_ball(im, self.pos_x, self.pos_y, 15, (0, 255, 255, 255))
