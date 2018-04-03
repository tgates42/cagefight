"""
The base fighter implementation
"""

from __future__ import absolute_import, print_function, division

from cagefight.cagefighter import CageFighter
import random
import math

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
        self.cooldown = 0
    @property
    def canfire(self):
        """
        Check if the gun is cool and we have the power to fire
        """
        return (
            1 if self.cooldown == 0 else 0
                and self.power > 30
        )
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
        if self.power <= 0:
            # dead
            return
        details = self.get_instructions(filepath)
        if self.cooldown > 0:
            self.cooldown -= 1
        if 'fire' in details:
            if self.canfire:
                self.power -= 30
                self.cooldown = 10
                radians = details['fire']
                proj = self.world.get_projectile()
                proj.owner = self.fighterid
                proj.posx = self.posx
                proj.posy = self.posy
                proj.deltax = math.cos(radians) * 5
                proj.deltay = math.sin(radians) * 5
                self.world.add_projectile(proj)
        else:
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
            'canfire': self.canfire,
            'cooldown': self.cooldown,
        }
    def save_view(self):
        """
        In addition to own details add details of food and players that are in sight
        """
        result = self.save()
        result['food'] = [
            food for food in self.world.food if (
                (food['x']- self.posx) ** 2
                + (food['y'] - self.posy) ** 2
            ) < 1600
        ]
        result['enemy'] = [
            {
                'x': fighter.posx,
                'y': fighter.posy,
            } for fighter in self.world.fighters if (
                    fighter.fighterid != self.fighterid
                and (
                    (fighter.posx - self.posx) ** 2
                    + (fighter.posy - self.posy) ** 2
                ) < 1600
                and fighter.power > 0
            )
        ]
        return result
    def load(self, jsonobj):
        """
        Deserialize current position
        """
        self.posx = jsonobj['x']
        self.posy = jsonobj['y']
        self.power = jsonobj['power']
        self.cooldown = jsonobj['cooldown']
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        if self.power <= 0:
            # dead
            return
        hs = self.size / 2
        self.world.draw_ball(im, self.posx - hs, self.posy - hs, self.size, self.colour)
    def collision(self, x, y):
        """
        Determine if a collision with the specified position has occurred.
        """
        return self.world.collision(x, y, self.posx, self.posy, self.size)
