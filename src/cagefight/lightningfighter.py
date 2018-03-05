"""
The base fighter implementation
"""

from __future__ import absolute_import, print_function, division

from cagefight.cagefighter import CageFighter
import random

class LightningFighter(CageFighter):
    """
    Lightning ball wars fighter
    """
    def __init__(self, world, fighterid):
        self.world = world
        self.fighterid = fighterid
        self.posx = None
        self.posy = None
        self.size = 10
        self.colour = CageFighter.colours[
            fighterid % len(CageFighter.colours)
        ]
        self.power = self.world.fighter_power
    def start(self):
        """
        Called prior to the first render to prepare the starting state.
        """
        hw = self.world.width / 2
        qw = self.world.width / 4
        hh = self.world.height / 2
        qh = self.world.height / 4
        self.posx = random.randint(qw, qw + hw)
        self.posy = random.randint(qh, qh + hh)
    def next(self, filepath):
        """
        Progress the game state to the next tick.
        """
        details = self.get_instructions(filepath)
        self.posx += max(-1, min(1, details.get('movex', 0)))
        self.posy += max(-1, min(1, details.get('movey', 0)))
    def save(self):
        """
        Serialize current position
        """
        return {
            'x': self.posx,
            'y': self.posy,
            'power': self.power,
        }
    def load(self, jsonobj):
        """
        Deserialize current position
        """
        self.posx = jsonobj['x']
        self.posy = jsonobj['y']
        self.power = jsonobj['power']
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        hs = self.size / 2
        self.world.draw_ball(im, self.posx - hs, self.posy - hs, self.size, self.colour)
    def collision(self, x, y):
        """
        Determine if a collision with the specified position has occurred.
        """
        return self.world.collision(x, y, self.posx, self.posy, self.size)
