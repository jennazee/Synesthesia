#!/usr/bin/python

from __future__ import division
import Image
import webcolors
from imagesimpler import ImageSimpler
from cooccurrence import CooccurrenceFinder
import copy
import string
from random import choice
from pygame import font, Surface
from pygame import image as PyImage
import sys


"""
** This module takes an image and replaces each pixel with a word that is associated with the color that pixel displays **
Concept: Natan Last
Execution: Jenna Zeigen (github.com/jennazee)

"""

class Synesthesizer():

	def synesthesize(self, image, colors, font):
		"""
		Purpose: Take an image, replace all the colors with words associated with the colors, saves the image to disk
		Inputs: Image to be adulterated, colors to be used
		Outputs: Nothing really -- saves image to disk
		"""

		#take the list of requested colors and get a "word palatte" for each word
		self.associates = {}
		self.storage = {}
		for color in colors:
			worder = CooccurrenceFinder()
			self.associates[color] = worder.find_relateds(worder.corpus_scraper(color, 20), [color], 15)[color]

		self.storage = copy.deepcopy(self.associates)

		#to be the word representation of the image
		textsize = 14

		font.init()
		self.texter = font.SysFont(font, textsize)
		
		(letWidth, letHeight) = self.texter.size('a')

		self.iSimp = ImageSimpler()
		self.preimg = self.iSimp.simplify(image, colors, 25)
		#self.preimg.save('simpleimg.jpg')
		self.img = self.preimg.resize((self.preimg.size[0], int(self.preimg.size[1]*(letWidth/letHeight))))
		pixor = self.img.load()

		newH = self.img.size[1]*letHeight
		newW = self.img.size[0]*letWidth

		self.synpic = Surface((newW, newH))
		self.synpic.fill((255,255,255))

		#replace pixel with words. One pixel -> one character.
		x = 0
		y = 0
		while y < self.img.size[1]:
			#what color is the current pixel?
			pixel = pixor[x,y]
			#ok, give me the associates
			wordsleft = self.associates[webcolors.rgb_to_name(pixel)]
			#get me the next word
			if len(wordsleft) > 0:
				word = wordsleft.pop()
			else:
				self.associates[webcolors.rgb_to_name(pixel)] = copy.deepcopy(self.storage[webcolors.rgb_to_name(pixel)])
				word = self.associates[webcolors.rgb_to_name(pixel)].pop()
			#do I have space left on the line?
			if len(word)+x <= self.img.size[0]:
				drawn = self.texter.render(word, True, pixel)
				self.synpic.blit(drawn, (x*letWidth,y*letHeight))
				x+=(len(word)+1)
				if x >= self.img.size[0]:
					y+=1
					x=0
			else:
				self.associates[webcolors.rgb_to_name(pixel)].append(word)
				y+=1
				x=0

		name = ''.join([choice(string.ascii_letters + string.digits) for n in range(30)])
		PyImage.save(self.synpic, 'creations/' +name + '.jpg')
		return 'creations/' +name + '.jpg'


def find_fonts():
	return font.get_fonts()

if __name__ == '__main__':
	syn = Synesthesizer()
	syn.synesthesize('rothko3.jpg', colors=['blue', 'black', 'orange'])