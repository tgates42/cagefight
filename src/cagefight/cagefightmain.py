"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

from cageworld import CageWorld
from cagedisplay import CageDisplay
import traceback

def main():
    """
    Main command line handler
    """
    try:
        world = CageWorld()
        outfile = '/var/out/output.mp4'
        display = CageDisplay(world, outfile)
        display.run()
        print('Complete')
    except:
        traceback.format_exc()
        print('Error')
        raise

if __name__ == '__main__':
    main()

