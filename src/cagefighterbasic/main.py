#!/usr/bin/env python
"""
Dumb fighter implementation
"""
from __future__ import print_function, division, absolute_import

import os
import json

def main(basedir):
    """
    Main entry point
    """
    with open(os.path.join(basedir, 'out.json'), 'w') as fobj:
        move = {'movex': 0, 'movey': 1}
        json.dump(move, fobj)
    print('Done.')

if __name__ == '__main__':
    main('/var/out')

