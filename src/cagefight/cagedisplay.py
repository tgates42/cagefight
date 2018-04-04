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
    def __init__(self, cageworld, outfile, csvfile):
        self.width = cageworld.width
        self.height = cageworld.height
        self.fps = cageworld.fps
        self.gameticks = cageworld.gameticks
        self.cageworld = cageworld
        self.outfile = outfile
        self.csvfile = csvfile
        self.background = cageworld.background
    def run(self, dirname):
        """
        Render the display to a mp4 output
        """
        writer = imageio.get_writer(self.outfile, fps=self.fps)
        self.cageworld.load_world_state(dirname, 'start')
        self.render(writer)
        for gametick in range(self.gameticks -  1):
            self.cageworld.load_world_state(
                dirname, 'step_%s' % (gametick,)
            )
            self.render(writer)
        writer.close()
        self.cageworld.save_csv_result(self.csvfile)
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
