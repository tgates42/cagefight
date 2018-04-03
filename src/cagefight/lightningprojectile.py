"""
The base projectile  implementation
"""

from __future__ import absolute_import, print_function, division

from cagefight.cageprojectile import CageProjectile

class LightningProjectile(CageProjectile):
    """
    Lightning ball wars projectile
    """
    def __init__(self, world):
        self.world = world
        self.owner = None
        self.posx = None
        self.posy = None
        self.deltax = None
        self.deltay = None
        self.size = 3
        self.colour = (255, 0, 0, 255)
    def next(self):
        """
        Progress the game state to the next tick.
        """
        self.posx += self.deltax
        self.posy += self.deltay
    def save(self):
        """
        Serialize current position
        """
        return {
            'owner': self.owner,
            'x': self.posx,
            'y': self.posy,
            'deltax': self.deltax,
            'deltay': self.deltay,
        }
    def load(self, jsonobj):
        """
        Deserialize current position
        """
        self.owner = jsonobj['owner']
        self.posx = jsonobj['x']
        self.posy = jsonobj['y']
        self.deltax = jsonobj['deltax']
        self.deltay = jsonobj['deltay']
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
