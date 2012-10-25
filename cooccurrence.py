#!/usr/bin/python

import re
import string
import numpy

import urllib2
from bs4 import BeautifulSoup
import json


class CooccurrenceFinder():

	def corpus_scraper(self, word, numdocs, redo=False):
		"""
		Purpose: Scrapes Wikipedia search results for a word and compiles all text to a single text file
		Inputs: Words to be searched for, number of documents to be scraped (the more the better the results), if corpuses for the word should be re-scraped due to changes in parameters, etc
		Outputs: The file path of the written file
		"""
		genCorpus = False
		try:
			open('corpuses/'+word+'_corpuses.txt')
		except IOError:
			genCorpus = True

		if genCorpus or redo:
			req = urllib2.Request(url='http://en.wikipedia.org/w/index.php?title=Special:Search&search='+str(word)+'&fulltext=Search&profile=advanced&redirs=1', headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15'})
			site = urllib2.urlopen(req)
			results = BeautifulSoup(site)
			site.close()

			anchors = []
			
			for link in results.find('ul', {'class':'mw-search-results'}).find_all('a')[0:numdocs]:
				anchors.append(link.get('href'))

			output = open('corpuses/'+word+'_corpuses.txt', 'w')
			for anchor in anchors:
				req = urllib2.Request(url='http://en.wikipedia.org'+str(anchor), headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15'})
				site = urllib2.urlopen(req)
				page = BeautifulSoup(site)
				site.close()
				output.write(page.find('div', {'class':'mw-body'}).get_text().encode('utf8')+'\n\n\n')

			output.close()

		return 'corpuses/'+word+'_corpuses.txt'

	#TODO: make this algorithm weighted by distance
	def find_relateds(self, corpus, words, distance):
		"""
		Purpose: To divine a list of words associated with each of word in a provided list as determined by a threshold of co-occurrence
		Inputs: The corpus to be analyzed, the words to be analyzed for, the max distance that would satisfy a co-occurrence
		Outputs: Significant co-occurrences
		"""

		#TODO: make it so that a newline wipes out the possibility of a 
		file = open(corpus, 'r')
		text = file.read().lower()
		file.close()

		file = open('stopword.txt', 'r')
		dump = file.read()
		file.close()
		stopwords = dump.split()

		#since this is being used for colors for now, I don't want, for example, 'blue' to be in 'red's' associate list
		stopwords.extend(['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'black', 'color', 'colors', 'colour', 'colours'])

		pairs = {}
		counts = {}
		sigCos = {}

		#building and executing the regex query, finding words that are a certain distance from the the target word
		for word in words:
			term = [word+'s?', r' (\w+)']
			pairs[word] = {}
			counts[word]={}
			for i in range(distance):
				if i is 0:
					pairs[word][i] = re.findall(''.join(term), text)
				else:
					term.insert(1, r' \w+')
					pairs[word][i] = re.findall(''.join(term), text)

				#figuring out number of occurrences -- FLAT for now
				#TODO: make it so that closer words carry more significance
				for targ in pairs[word][i]:
					if stopwords.count(targ)>0 or re.search(word, targ):
						continue
					elif targ in counts[word]:
						counts[word][targ]+=1
					else:
						counts[word][targ]=1

		##see if any of the words occur >1.96 SDs from the mean, or outside of a 95% tolerance interval
		for word in words:
			sigCos[word]=[]
			allCounts = []
			for coll in counts[word].keys():
				allCounts.append(counts[word][coll])
			av = numpy.average(allCounts)
			std = numpy.std(allCounts)
			for coll in counts[word].keys():
				if (counts[word][coll]-av)/std > 1.96:
					sigCos[word].append(coll)

		return sigCos

if __name__ == '__main__':
	cf = CooccurrenceFinder()
	cf.find_relateds(cf.corpus_scraper('cat', 5),['cat'], 50)	