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
        config = configparser.ConfigParser()
        config.read('/etc/default.ini')
        world = CageWorld.load(config)
        if not os.path.isdir('/var/out'):
            os.makedirs('/var/out')
        with open('/var/out/run.sh', 'w') as fobj:
            world.save_runsheet(fobj)
        print('Complete')
    except:
        traceback.format_exc()
        print('Error')
        raise

if __name__ == '__main__':
    main()

