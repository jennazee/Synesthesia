#!/usr/bin/python
from __future__ import division
from math import floor, ceil
import string
import sys
from random import choice, shuffle, randint
from collections import defaultdict, deque
import pickle

import Image
import webcolors
from imagesimpler import ImageSimpler
from cooccurrence import CooccurrenceFinder
from pygame import font, Surface
from pygame import image as PyImage


"""
** This module takes an image and replaces each pixel with a word that is associated with the color that pixel displays **
Concept: Natan Last
Execution: Jenna Zeigen (github.com/jennazee)

"""

class Synesthesizer():

    def combinatorics(self):
        """
        Purpose: Creates a file containing a pickled dictionary, keyed by color words, of strings containing associates that are up to 25 characters long
        Inputs: None
        Outputs: Nothing explicit
        """
        self.color_stops = ['red', 'orange', 'yellow', 'green', 'brown', 'blue', 'purple', 'pink', 'white', 'black', 'color', 'grey', 'gray' 'colors', 'colour', 'colours', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.colors = ['red', 'orange', 'yellow', 'green', 'brown', 'blue', 'purple', 'pink', 'black', 'grey']
        self.associates = {}
        self.all_combos = {}
        self.max_length = 25

        for color in self.colors:
            worder = CooccurrenceFinder()
            self.associates[color] = worder.find_relateds(worder.corpus_scraper(color, 20), color, 15, self.color_stops, 1.96)

        for key in self.associates:
            col_combos = defaultdict(deque)
            for el in self.associates[key]:
                temp = defaultdict(list)
                leng = len(el) + 1
                for le in col_combos:
                    if le < self.max_length - leng:
                        for item in col_combos[le]:
                            temp[le+leng].append(item + el + ' ')
                for length in temp:
                    col_combos[length].extend(temp[length])
                col_combos[leng].append(el + ' ')

            for k in col_combos:
                shuffle(col_combos[k])

            self.all_combos[key] = col_combos

        f = open('combos', 'w')
        pickle.dump(self.all_combos, f)
        f.close()

    def reconstitute(self):
        f = open('combos', 'r')
        self.all_combos = pickle.load(f)
        f.close()
        
    def synesthesize(self, image, colors, fontname):
        """
        Purpose: Take an image, replace all the colors with words associated with the colors, saves the image to disk
        Inputs: Image to be adulterated, colors to be used
        Outputs: Filename of created image
        """
        textsize = 14

        font.init()
        self.texter = font.SysFont(fontname, textsize)
        
        (letWidth, letHeight) = self.texter.size('a')

        self.iSimp = ImageSimpler()
        self.preimg = self.iSimp.simplify(image, colors, 25)
        self.img = self.preimg.resize((self.preimg.size[0], int(self.preimg.size[1]*(letWidth/letHeight))))
        pixor = self.img.load()

        newH = self.img.size[1]*letHeight
        newW = self.img.size[0]*letWidth

        self.synpic = Surface((newW, newH))
        self.synpic.fill((255,255,255))

        #replace pixels with words. One pixel -> one character. Oh hai, linear packing approximation...
        x = 0
        y = 0

        def check_fit(space, color):
            if space <= 25:
                if self.all_combos[color][space]:
                    word = self.all_combos[color][space].pop()
                    self.all_combos[color][space].appendleft(word)
                    return word
                else:
                    if space>=8:
                        return check_fit(floor(space/2), color) + check_fit(ceil(space/2), color)
                    else:
                        return "!"*int(space)

            else:
                shift = randint(0,4)
                return check_fit(floor(space/2)-shift, color) + check_fit(ceil(space/2)+shift, color)


        def get_space(x,y, color):
            x1 = x
            while x<self.img.size[0] and webcolors.rgb_to_name(pixor[x,y]) is color:
                x+=1
            return x-x1

        def paint_picture(x, y):
            while y < self.img.size[1]:
                pixel = pixor[x,y]
                color = webcolors.rgb_to_name(pixel)
                space = get_space(x,y, color)

                string = check_fit(space, color)
                drawn = self.texter.render(string, True, pixel)
                self.synpic.blit(drawn, (x*letWidth,y*letHeight))
                x+=(len(string))
                if x >= self.img.size[0]:
                    y+=1
                    x=0

        paint_picture(x,y)

        name = ''.join([choice(string.ascii_letters + string.digits) for n in range(30)])
        PyImage.save(self.synpic, 'creations/' +name + '.jpg')

        return 'creations/' +name + '.jpg'

def find_fonts():
    monospaced = ["bitstreamverasansmono", "consolas", "luximono", "lucidaconsole", "andalemono", "couriernew", 'inconsolata', 'courier', 'monaco']
    return sorted([f for f in font.get_fonts() if f in monospaced])

if __name__ == '__main__':
    syn = Synesthesizer()
    syn.reconstitute()
    syn.synesthesize('rothko3.jpg', ['blue', 'green', 'black', 'orange'], 'couriernew')