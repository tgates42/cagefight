"""
Main entry point for cage fight controller
"""

from __future__ import absolute_import, print_function, division

import imageio
import numpy
from PIL import Image

class CageDisplay(object):
    """
    Display for the game state to render mp4 output
    """
    def __init__(self, cageworld, outfile):
        self.width = cageworld.width
        self.height = cageworld.height
        self.fps = cageworld.fps
        self.gameticks = cageworld.gameticks
        self.cageworld = cageworld
        self.outfile = outfile
        self.background = cageworld.background
    def run(self):
        """
        Render the display to a mp4 output
        """
        writer = imageio.get_writer(self.outfile, fps=self.fps)
        self.cageworld.start()
        self.render(writer)
        for _ in range(self.gameticks -  1):
            self.cageworld.next()
            self.render(writer)
        writer.close()
    def render(self, writer):
        """
        Obtain an image of the current state and save it to the movie writer
        """
        writer.append_data(numpy.asarray(self.get_image()))
    def get_image(self):
        """
        Render an image for the display at the specified tick
        """
        im = Image.new('RGBA', (self.width, self.height), self.background)
        self.cageworld.render(im)
        return im
