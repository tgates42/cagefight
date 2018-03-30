"""
Tests for the lightning world game
"""

import unittest

class LightningWorld_Test(unittest.TestCase):
    """
    Tests for the lightning world game
    """
    def test_fighter_save(self):
        """
        Given a known world state check the fighter view saves correctly.
        """
        # Setup
        from cagefight.lightningworld import LightningWorld
        import configparser
        config = configparser.ConfigParser()
        fighterid = 0
        world = LightningWorld(config)
        world.start()
        world.fighters[fighterid].posx = 200
        world.fighters[fighterid].posy = 195
        world.food = [{'x': 210, 'y': 190}, {'x': 410, 'y': 405}]
        world.fighters[1].posx = 220
        world.fighters[1].posy = 180
        # Exercise
        jsonobj = world.save_fighter_world_to_json(fighterid)
        # Verify
        assert jsonobj == {
            'food': [{'x': 210, 'y': 190}],
            'enemy': [{'x': 220, 'y': 180}],
            'power': 500,
            'x': 200,
            'y': 195,
        }
