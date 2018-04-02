#!/usr/bin/env python
"""
Dumb fighter implementation
"""
from __future__ import print_function, division, absolute_import

import os
import json
import operator
import math

def main(basedir):
    """
    Main entry point
    """
    with open(os.path.join(basedir, 'world.json')) as fobj:
        world = json.load(fobj)
        posx = world['x']
        posy = world['y']
        power = world['power']
        foods = world['food']
        enemies = world['enemy']
        canfire = world['canfire']
        for food in foods:
            food['dist'] = (
                ((food['x'] - posx) ** 2)
                + ((food['y'] - posy) ** 2)
            )
        foods.sort(key=operator.itemgetter('dist'))
        for enemy in enemies:
            enemy['dist'] = (
                ((enemy['x'] - posx) ** 2)
                + ((enemy['y'] - posy) ** 2)
            )
        enemies.sort(key=operator.itemgetter('dist'))
    with open(os.path.join(basedir, 'out.json'), 'w') as fobj:
        if enemies and power > 200 and canfire:
            move = {
                'fire': math.atan2(
                    enemies[0]['y'] - posy, enemies[0]['x'] - posx
                )
            }
        elif foods:
            move = {
                'movex': foods[0]['x'] - posx,
                'movey': foods[0]['y'] - posy,
            }
        else:
            move = {'movex': 200 - posx, 'movey': 200 - posy}
        json.dump(move, fobj)
    print('Done.')

if __name__ == '__main__':
    main('/var/out')

