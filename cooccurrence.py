import re
import string
import numpy

import urllib2
from bs4 import BeautifulSoup
import json


class CooccurrenceFinder():

	def corpus_scraper(self, word, numdocs):
		"""
		Purpose: Scrapes Wikipedia search results for a word and compiles all text to a single text file
		Inputs: Words to be searched for, number of documents to be scraped (the more the better the results)
		Outputs: The file path of the written file
		"""

		req = urllib2.Request(url='http://en.wikipedia.org/w/index.php?title=Special:Search&search='+str(word)+'&fulltext=Search&profile=advanced&redirs=1', headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15'})
		site = urllib2.urlopen(req)
		results = BeautifulSoup(site)
		site.close()

		anchors = []
		
		for link in results.find('ul', {'class':'mw-search-results'}).find_all('a')[0:numdocs]:
			anchors.append(link.get('href'))

		output = open(str(word)+'_corpuses.txt', 'w')
		for anchor in anchors:
			req = urllib2.Request(url='http://en.wikipedia.org'+str(anchor), headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15'})
			site = urllib2.urlopen(req)
			page = BeautifulSoup(site)
			site.close()
			output.write(page.find('div', {'class':'mw-body'}).get_text().encode('utf8')+'\n\n\n')

		output.close()

		return str(word)+'_corpuses.txt'

	#TODO: make this algorithm weighted by distance
	def find_relateds(self, corpus, words, distance):
		"""
		Purpose: To divine a list of words associated with each of word in a provided list as determined by a threshold of co-occurrence
		Inputs: The corpus to be analyzed, the words to be analyzed for, the max distance that would satisfy a co-occurrence
		Outputs: Significant co-occurrences
		"""

		#TODO: make it so that a newline wipes out the possibility of a 
		#m = re.findall(r'amendments? (\w+)', text)

		file = open(corpus, 'r')
		text = file.read().lower()
		file.close()

		file = open('stopword.txt', 'r')
		dump = file.read()
		file.close()
		stopwords = dump.split()

		stopwords.extend(['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'white', 'black', 'color', 'colors', 'colour', 'colours'])

		#making lists of words
		pairs = {}
		counts = {}
		sigCos = {}

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
				for targ in pairs[word][i]:
					if stopwords.count(targ)>0 or targ==word:
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

		print sigCos

if __name__ == '__main__':
	cf = CooccurrenceFinder()
	cf.find_relateds(cf.corpus_scraper('cat', 5),['cat'], 50)
	