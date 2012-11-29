#!/usr/bin/python
import re
import string
import json
import urllib2

from bs4 import BeautifulSoup
import numpy


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
    def find_relateds(self, corpus, word, distance, extra_stops, stdevs):
        """
        Purpose: To divine a list of words associated with a provided word as determined by a threshold of co-occurrence
        Inputs: The corpus to be analyzed, the words to be analyzed for, the max distance that would satisfy a co-occurrence
        Outputs: Significant co-occurrences
        """

        #TODO: make it so that a newline wipes
        file = open(corpus, 'r')
        text = file.read().lower()
        file.close()

        file = open('stopword.txt', 'r')
        dump = file.read()
        file.close()
        stopwords = dump.split()

        #since this is being used for colors for now, I don't want, for example, 'blue' to be in 'red's' associate list
        stopwords.extend(extra_stops)

        self.counts = {}

        pairs = self.find_close_words(distance, text, word)

        for i in range(distance):
            self.tally_occurrences(word, pairs[i], stopwords)

        return self.find_significant_cooccurrences(self.counts, stdevs)


    #TODO: add before word functionality
    def find_close_words(self, dist, text, word):
        """
        Purpose: Finds all the words in a corpus within a specified distance of a target word
        Inputs: Desired distance, text corpus, target word
        Outputs: Dictionary of distances to words that distance after the target
        """
        term = [word+'s?', r' (\w+)']
        temp_pairs = {}
        for i in range(dist):
            if i is 0:
                temp_pairs[i] = re.findall(''.join(term), text)
            else:
                term.insert(1, r' \w+')
                temp_pairs[i] = re.findall(''.join(term), text)

        return temp_pairs

    #TODO: make it so that closer words carry more significance
    def tally_occurrences(self, word, pair_set, stopwords):
        """
        Purpose: Create a frequency distribution for the area after the target word, but not including stop words or derivatives of the target
        Inputs: Target word, dictionary of distances to words, stopwords
        Outputs: Nothing explicitly
        """
        for targ in pair_set:
            if stopwords.count(targ)>0 or re.search(word, targ):
                continue
            elif targ in self.counts:
                self.counts[targ]+=1
            else:
                self.counts[targ]=1

    def find_significant_cooccurrences(self, counts, SDs):
        """
        Purpose: The find the significant co-occurrences from a frequency distribution
        Inputs: Frequency distribution, number of standard deviations for signficance
        Outputs: List of significant cooccurrences
        """
        allCounts = []
        sigCos = []
        for coll in counts.keys():
            allCounts.append(counts[coll])
        av = numpy.average(allCounts)
        std = numpy.std(allCounts)
        for coll in counts.keys():
            if (counts[coll]-av)/std > SDs:
                sigCos.append(coll)

        return sigCos

if __name__ == '__main__':
    cf = CooccurrenceFinder()
    cf.find_relateds(cf.corpus_scraper('dog', 5),'dog', 50, ['dog'], 1.96)  