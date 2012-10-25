#!/usr/bin/python

import Image
import webcolors
from imagesimpler import ImageSimpler
from cooccurrence import CooccurrenceFinder
import copy
from pygame import font, Surface
from pygame import image as PyImage

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
		print 'Simplifying the Image'

		iSimp = ImageSimpler()
		img = iSimp.simplify(image, colors, 25)
		pixor = img.load()
		img.show()

		#take the list of requested colors and get a "word palatte" for each word
		associates = {}
		storage = {}
		for color in colors:
			print 'Building associates for ' + str(color)
			worder = CooccurrenceFinder()
			associates[color] = worder.find_relateds(worder.corpus_scraper(color, 20), [color], 15)[color]

		storage = copy.deepcopy(associates)

		#to be the word representation of the image
		textsize = 12

		font.init()
		texter = font.SysFont('couriernew', textsize)
		
		(letWidth, letHeight) = texter.size('A')

		newH = img.size[1]*letHeight
		newW = img.size[0]*letWidth

		synpic = Surface((newW, newH))
		synpic.fill((255,255,255))

		#replace pixel with words. One pixel -> one character.
		x = 0
		y = 0
		print 'Drawing Image'
		while y < img.size[1]:
			#what color is the current pixel?
			pixel = pixor[x,y]
			#ok, give me the associates
			wordsleft = associates[webcolors.rgb_to_name(pixel)]
			#get me the next word
			if len(wordsleft) > 0:
				word = wordsleft.pop()
			else:
				associates[webcolors.rgb_to_name(pixel)] = copy.deepcopy(storage[webcolors.rgb_to_name(pixel)])
				word = associates[webcolors.rgb_to_name(pixel)].pop()
			#do I have space left on the line?
			if len(word)+x <= img.size[0]:
				drawn = texter.render(word, True, pixel)
				synpic.blit(drawn, (x*letWidth,y*letHeight))
				x+=(len(word)+1)
				if x >= img.size[0]:
					y+=1
					x=0
			else:
				associates[webcolors.rgb_to_name(pixel)].append(word)
				y+=1
				x=0

		PyImage.save(synpic, 'output.jpg')

if __name__ == '__main__':
	syn = Synesthesizer()
	syn.synesthesize('rothko3.jpg', colors=['blue', 'black', 'orange'])