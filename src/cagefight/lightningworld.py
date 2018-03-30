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
        self.food = []
        self.food_probability = config.getfloat(
            'lightning', 'food_probability',
            fallback=0.1,
        )
        self.food_power = config.getint(
            'lightning', 'food_power', fallback=50,
        )
        self.fighter_power = config.getint(
            'lightning', 'start_power', fallback=500,
        )
    def get_fighter(self, fighterid):
        """
        Prepare the fighter implementation
        """
        from cagefight.lightningfighter import LightningFighter
        return LightningFighter(self, fighterid)
    def next(self, basedir, gametick):
        super(LightningWorld, self).next(basedir, gametick)
        foodcheck = random.random()
        if foodcheck < self.food_probability:
            self.gen_food()
        self.eat()
    def eat(self):
        """
        Check if any players are near food and if so they consume the power
        """
        result = []
        for fooditem in self.food:
            drop = False
            for fighter in self.fighters:
                if fighter.collision(
                            fooditem['x'], fooditem['y'],
                        ):
                    fighter.power += self.food_power
                    drop = True
                    break
            if not drop:
                result.append(fooditem)
        self.food = result
    def gen_food(self):
        """
        Create a power ball randomly in the world.
        """
        self.food.append({
            'x': random.randint(0, self.width),
            'y': random.randint(0, self.height),
        })
    @classmethod
    def kind(cls):
        """
        Overridden to provide a world kind key
        """
        return 'lightning'
    def save_world_to_json(self):
        """
        serialize game state
        """
        result = super(LightningWorld, self).save_world_to_json()
        result['food'] = self.food
        return result
    def save_fighter_world_to_json(self, fighterid):
        """
        serialize single player game view
        """
        result = super(
            LightningWorld, self
        ).save_fighter_world_to_json(fighterid)
        return result
    def load_world_from_json(self, jsonobj):
        """
        deserialize game state
        """
        super(LightningWorld, self).load_world_from_json(jsonobj)
        self.food = jsonobj.get('food', [])
    def render(self, im):
        """
        Display world
        """
        super(LightningWorld, self).render(im)
        self.render_food(im)
    def render_food(self, im):
        """
        Display power balls
        """
        for food in self.food:
            self.draw_ball(
                im, food['x'] - 2, food['y'] - 2, 4, (0, 255, 0, 255)
            )
