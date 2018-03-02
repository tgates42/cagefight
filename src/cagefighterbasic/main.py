#!/usr/bin/env python

import os

def main(basedir):
    print(repr(os.listdir(basedir)))
    print('Done.')

if __name__ == '__main__':
    main('/var/out')

