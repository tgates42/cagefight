#!/usr/bin/env python
"""\
%(app)s

Usage:
   %(cmd)s [options] [<args>...]
   %(cmd)s (-h | --help)
   %(cmd)s --version

Options:
  -h --help              Show this screen
  --version              Show version
  --start                Begin the world
  --step=<n>             Execute the specified step
  --render               Draw the world`
"""
# vi:syntax=python

from __future__ import absolute_import, print_function, division

import traceback
import configparser
import os
import sys
import docopt

__appname__ = 'cagefight'
__version__ = '0.1'

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
    appname = __appname__ if __appname__ else sys.argv[0]
    args = docopt.docopt(
        __doc__ % {
            'app': appname,
            'cmd': sys.argv[0],
        },
        version='%s %s' % (
            appname,
            __version__,
        )
    )
    return args

def main():
    """
    Main command line handler
    """
    try:
        args = setup()
        from cagefight.cageworld import CageWorld
        config = configparser.ConfigParser()
        config.read('/etc/default.ini')
        world = CageWorld.load(config)
        if args['--render']:
            render(world)
        print('Complete')
    except:
        traceback.format_exc()
        print('Error')
        raise

def render(world):
    """
    Produce the video output
    """
    from cagefight.cagedisplay import CageDisplay
    outfile = '/var/out/output.mp4'
    display = CageDisplay(world, outfile)
    display.run()

if __name__ == '__main__':
    main()

