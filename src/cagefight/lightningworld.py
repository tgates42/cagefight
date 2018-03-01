"""
A very simple game involving lightning spheres that can attack each other
"""

from __future__ import absolute_import, print_function, division

from cagefight.cageworld import CageWorld

class LightningWorld(CageWorld):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self, config):
        super(LightningWorld, self).__init__(config)
    def get_fighter(self, fighterid):
        """
        Prepare the fighter implementation
        """
        from cagefight.lightningfighter import LightningFighter
        return LightningFighter(self, fighterid)
    @classmethod
    def kind(cls):
        """
        Overridden to provide a world kind key
        """
        return 'lightning'
