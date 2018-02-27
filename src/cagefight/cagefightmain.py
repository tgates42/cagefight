"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

import imageio

def main():
    """
    Main command line handler
    """
    open('/var/out/x', 'w').close()
    print('ok')
    im = imageio.imread('imageio:chelsea.png')
    writer = imageio.get_writer('/var/out/output.mp4', fps=25)
    for _ in range(125):
        writer.append_data(im)
    writer.close()


if __name__ == '__main__':
    main()

