"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

import os

def main():
    """
    Main command line handler
    """
    print(repr(list(os.walk('/'))))


if __name__ == '__main__':
    main()

