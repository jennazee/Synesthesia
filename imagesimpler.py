#!/usr/bin/python
from os import path

import Image
import webcolors



class ImageSimpler():
    """
    Purpose: To take an image and "round" all colors to one of a specified list of colors and then return the mutated image
    Inputs: image to be manipulated, colors to be "rounded to", scaled size of the image
    Outputs: The mutated image
    """

    def simplify(self, imagefile, colors, percentsize):
        """
        Purpose: To take an image, scale it as specified, and "round" all colors to one of a specified list of colors and then return the mutated image
        Inputs: Image to be manipulated, colors to be "rounded to", scaled size of the image
        Outputs: The mutated image
        """
        n, e = path.splitext(imagefile)
        
        if e.lower() not in ['.jpg', '.jpeg', '.png']:
            raise Exception('Image type not supported')
        print e.lower() == '.png', e.lower(), '.png'
        if e.lower() == '.png':
            print 'image converted'
            Image.open(imagefile).save(n + '.jpg')
        self.image = Image.open(n + '.jpg')
        if percentsize is not 100:
            self.image = self.scale_by_percent(self.image, percentsize)

        self.color_map = self.map_RGB_to_color_word(colors)

        #makes the image more readily mutable and readable by creating a "Pixel Access Object"
        self.pixels = self.image.load()

        return self.reduce_to_requested_color_space(self.pixels, self.image, self.color_map)


    def scale_by_percent(self, im, percent):
        """
        Purpose: Scale an image to a specified size
        Inputs: Image, desired percent size
        Outputs: Scaled image
        """
        newx = int(im.size[0]*(percent/100.00))
        newy = int(im.size[1]*(percent/100.00))
        return im.resize((newx, newy))

    def map_RGB_to_color_word(self, colors):
        """
        Purpose: Creates a mapping of rgb colors to "css colors"
        Inputs: List of css colors
        Outputs: Dictionary of rgbs to css colors
        """
        rgbsToColors = {}
        for color in colors:
            rgbsToColors[webcolors.name_to_rgb(color)] = color
        return rgbsToColors

    def reduce_to_requested_color_space(self, pix_obj, im, color_mapping):
        """
        Purpose: Creates an image in which colors are changed to be whatever they are closest to from a list of colors
        Inputs: PIL pixel object, image, dictionary of rgbs to css colors
        Outputs: Color-simplified image
        """
        print pix_obj
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                pix = pix_obj[x,y]
                #initial settings soon to be overridden
                closest = None
                mindist = float('Inf')
                #find which rgb triplet is the closest through Euclidean distance of their vectors
                for rgb in color_mapping:
                    dist = (rgb[0]-pix[0])*(rgb[0]-pix[0])+(rgb[1]-pix[1])*(rgb[1]-pix[1])+(rgb[2]-pix[2])*(rgb[2]-pix[2])
                    if dist < mindist:
                        mindist = dist
                        closest = rgb
                pix_obj[x,y] = closest
        return im