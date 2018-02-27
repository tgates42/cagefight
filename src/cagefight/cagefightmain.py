"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

import imageio
import numpy
from PIL import Image, ImageDraw

def main():
    """
    Main command line handler
    """
    display = CageDisplay()
    display()

class CageDisplay(object):
    """
    Display for the game state to render mp4 output
    """
    def __call__(self):
        """
        Render the display to a mp4 output
        """
        writer = imageio.get_writer('/var/out/output.mp4', fps=25)
        for tick in range(125):
            writer.append_data(numpy.asarray(self.get_image(tick)))
        writer.close()
    def get_image(self, tick):
        """
        Render an image for the display at the specified tick
        """
        im = Image.new('RGBA', (480, 480), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.line((tick, 0, im.size[0] - tick, im.size[1]), fill=128)
        draw.line((0, im.size[1] - tick, im.size[0], tick), fill=128)
        return im

if __name__ == '__main__':
    main()

