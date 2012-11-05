#!/usr/bin/python
import Image
import webcolors
import math


class ImageSimpler():
	"""
	Purpose: To take an image and "round" all colors to one of a specified list of colors and then return the mutated image
	Inputs: image to be manipulated, colors to be "rounded to", scaled size of the image
	Outputs: The mutated image
	"""

	def simplify(self, imagefile, colors, percentsize):
		self.image = Image.open(imagefile)
		if percentsize is not 100:
			self.image = self.scale_by_percent(self.image, percentsize)

		self.color_map = self.map_RGB_to_color_word(colors)

		#makes the image more readily mutable and readable by creating a "Pixel Access Object"
		self.pixels = self.image.load()

		return self.reduce_to_requested_color_space(self.pixels, self.image, self.color_map)


	def scale_by_percent(self, im, percent):
		newx = int(im.size[0]*(percent/100.00))
		newy = int(im.size[1]*(percent/100.00))
		return im.resize((newx, newy))

	def map_RGB_to_color_word(self, colors):
		rgbsToColors = {}
		for color in colors:
			rgbsToColors[webcolors.name_to_rgb(color)] = color
		return rgbsToColors

		
	def reduce_to_requested_color_space(self, pix_obj, im, color_mapping):
		for x in range(im.size[0]):
			for y in range(im.size[1]):
				pix = pix_obj[x,y]
				#initial settings soon to be overridden
				closest = None
				mindist = float('Inf')
				#find which rgb triplet is the closest through Euclidean distance of their vectors
				for rgb in color_mapping:
					dist = math.sqrt((rgb[0]-pix[0])*(rgb[0]-pix[0])+(rgb[1]-pix[1])*(rgb[1]-pix[1])+(rgb[2]-pix[2])*(rgb[2]-pix[2]))
					if dist < mindist:
						mindist = dist
						closest = rgb
				pix_obj[x,y] = closest
		return im