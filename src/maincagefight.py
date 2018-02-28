"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

import traceback
import configparser
import os
import sys

def get_basedir():
    """
    Locate the current directory of this file
    """
    return os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))

def setup():
    """
    Add the current path to the classpath
    """
    sys.path.append(get_basedir())

def main():
    """
    Main command line handler
    """
    try:
        setup()
        from cagefight.cageworld import CageWorld
        from cagefight.cagedisplay import CageDisplay
        config = configparser.ConfigParser()
        config.read('/etc/default.ini')
        world = CageWorld.load(config)
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

