#!/usr/bin/python

import Image
import webcolors
from imagesimpler import ImageSimpler
from cooccurrence import CooccurrenceFinder
import copy

"""
** This module takes an image and replaces each pixel with a word that is associated with the color that pixel displays **
Concept: Natan Last
Execution: Jenna Zeigen (github.com/jennazee)

"""

class Synesthesizer():

	def synesthesize(self, image, colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'black', 'gray']):
		"""
		Purpose: Take an image, replace all the colors with words associated with the colors, saves the image to disk
		Inputs: Image to be adulterated, colors to be used
		Outputs: Nothing really -- saves image to disk
		"""

		iSimp = ImageSimpler()
		image = iSimp.simplify(image, colors, 10)
		pixor = image.load()

		#take the list of requested colors and get a "word palatte" for each word
		associates = {}
		storage = {}
		for color in colors:
			worder = CooccurrenceFinder()
			#associates[color] = worder.find_relateds(worder.corpus_scraper(color, 20), color, 15)
			associates[color] = worder.find_relateds(str(color)+'_corpuses.txt', [color], 15)[color]

		storage = copy.deepcopy(associates)

		#to be the word representation of the image
		wordArray = []

		#replace each pixel with a word
		for y in range(image.size[1]):
			line = []
			for x in range(image.size[0]):
				pixel = pixor[x,y]
				wordsleft = associates[webcolors.rgb_to_name(pixel)]
				if len(wordsleft) > 0:
					line.append(wordsleft.pop())
				else:
					associates[webcolors.rgb_to_name(pixel)] = copy.deepcopy(storage[webcolors.rgb_to_name(pixel)])
					line.append(associates[webcolors.rgb_to_name(pixel)].pop())
			wordArray.append(line)

		print wordArray


if __name__ == '__main__':
	syn = Synesthesizer()
	syn.synesthesize('../lime-cat.jpg', colors=['orange', 'green'])