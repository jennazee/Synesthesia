#!/usr/bin/python

import Image
import webcolors
import ImageSimpler
import CooccurrenceFinder

class Synesthesizer():

	def synesthesize(self, image, colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'black', 'gray']):
		"""
		Purpose: Take an image, replace all the colors with words associated with the colors, saves the image to disk
		Inputs: Image to be adulterated, colors to be used
		Outputs: Nothing really -- saves image to disk
		"""

		iSimp = ImageSimpler()
		image = iSimp.simplify(image, colors, 25)
		pixor = image.load()

		associates = {}
		for color in colors:
			worder = CooccurrenceFinder()
			associates[color] = worder.find_relateds(worder.corpus_scraper(color, 20), color, 15)

		print associates

		# wordArray = []

		# for y in range(image.size[1]):
		# 	line = []
		# 	for x in range(image.size[0]):
		# 		pix = pixor[x,y]

if __name__ == '__main__':
	syn = Synesthesizer()
	syn.synesthesize('../lime-cat.jpg')