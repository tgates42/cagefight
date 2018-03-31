#!/usr/bin/env python
"""
Dumb fighter implementation
"""
from __future__ import print_function, division, absolute_import

import os
import json
import operator

def main(basedir):
    """
    Main entry point
    """
    with open(os.path.join(basedir, 'world.json')) as fobj:
        world = json.load(fobj)
        posx = world['x']
        posy = world['y']
        foods = world['food']
        for food in foods:
            food['dist'] = (
                ((food['x'] - posx) ** 2)
                + ((food['y'] - posy) ** 2)
            )
        foods.sort(key=operator.itemgetter('dist'))
    with open(os.path.join(basedir, 'out.json'), 'w') as fobj:
        if foods:
            move = {
                'movex': posx - foods[0]['x'],
                'movey': posy - foods[0]['y'],
            }
        else:
            move = {'movex': 0, 'movey': 1}
        json.dump(move, fobj)
    print('Done.')

if __name__ == '__main__':
    main('/var/out')

