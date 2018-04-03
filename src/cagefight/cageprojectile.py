"""
Base class for a projectile
"""

class CageProjectile(object):
    """
    Simple projectile base class
    """
    def __init__(self, world, projectileid):
        self.world = world
        self.projectileid = projectileid
    def next(self):
        """
        Progress the game state to the next tick.
        """
        pass
    def save(self):
        """
        Override to save details of current projectile with total knowledge
        """
        raise NotImplementedError('Override to save projectile')
    def load(self, jsonobj):
        """
        Override to load details of current projectile
        """
        raise NotImplementedError('Override to load projectile')
    def render(self, im):
        """
        Render the display to an image for the provided game mp4 output
        """
        raise NotImplementedError('Override to draw projectile')
