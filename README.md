#Synesthesia
Takes in an image and replace the colors with words semantically related to the color.

Project in action: <http://www.jennazeigen.com/Synesthesia>

So, if there's a red patch in your image, in that area in the resulting image, you might find the words "cherry", "communism", "anger", and "balloon"

Concept: Natan Last, Execution: Jenna Zeigen (me!)

I've blogged about this project and more how each of the methods work at <http://linkguistics.blogspot.com/2012/12/project-synesthesia.html>

##Components:
1. cooccurrence.py -- This is the module that makes the lists of words are associated with the colors.
2. imagesimpler.py -- This module reduces the color space so that the words can be properly associated with the colors
3. synesthesizer.py -- This module takes the words and image and maps them, creating the final piece
4. synserver.py -- Flask-powered; Makes synesthesizer a web app with a pretty GUI with the help of syn.js and syn.css

--------
##GUI
![Initial Screen](http://www.jennazeigen.com/Github-Readme-Imgs/initial.png "Initial Screen")

While synthesizer.py also works as a command line tool, it also has a web app interface powered by Flask. You upload your image, which will them be previewed, and then choose all the conditions to modify the parameters.

![GUI shown with preview of uploaded image](http://www.jennazeigen.com/Github-Readme-Imgs/upload.png "Preview of uploaded image")


When you submit your image and choices, the result will appear and you can then click on the preview to download the image.

![GUI shown with resulting image](http://www.jennazeigen.com/Github-Readme-Imgs/output_better.png "Showing the resulting image")

--------
##API
###cooccurrence.py
* Finds words within a corpus that cooccur significantly with a target word
* Dependencies: BeautifulSoup4 and numpy

####`CooccurrenceFinder()`

#####`corpus_scraper(self, word, numdocs, redo=False)`
* Purpose: Scrapes Wikipedia search results for a word and compiles all text to a single text file
* Inputs: Words to be searched for, number of documents to be scraped (the more the better the results), if corpuses for the word should be re-scraped due to changes in parameters, etc
* Outputs: The file path of the written file

#####`find_relateds(self, corpus, word, distance, extra_stops, stdevs)`
* Purpose: To divine a list of words associated with a provided word as determined by a threshold of co-occurrence
* Inputs: The corpus to be analyzed, the words to be analyzed for, the max distance that would satisfy a co-occurrence, extra stop words (domain specific?), standard deviation threshold for significance
* Outputs: Significant co-occurrences

#####`find_close_words(self, dist, text, word)`
* Purpose: Finds all the words in a corpus within a specified distance of a target word
* Inputs: Desired distance, text corpus, target word
* Outputs: Dictionary of distances to words that distance from the target

#####`tally_occurrences(self, word, pair_set, stopwords)`
* Purpose: Create a frequency distribution for the area surrounding the target word, but not including stop words or derivatives of the target
* Inputs: Target word, dictionary of distances to words, stopwords
* Outputs: Nothing explicitly

#####`find_significant_cooccurrences(self, counts, SDs)`
* Purpose: The find the significant co-occurrences from a frequency distribution
* Inputs: Frequency distribution, number of standard deviations for signficance
* Outputs: List of significant cooccurrences

-------------------------

###imagesimpler.py
* Simplifies the color space of an image to a specified space
* Dependencies: pillow and webcolors

####`ImageSimpler()`:
#####`simplify(self, imagefile, colors, percentsize)`
* Purpose: To take an image, scale it as specified, and "round" all colors to one of a specified list of colors and then return the mutated image. Only takes jpeg and png. Otherwise, throws an Exception.
* Inputs: Image to be manipulated, colors to be "rounded to", scaled size of the image
* Outputs: The mutated image

#####`scale_by_percent(self, im, percent)`
* Purpose: Scale an image to a specified size
* Inputs: Image, desired percent size
* Outputs: Scaled image

#####`map_RGB_to_color_word(self, colors)`
* Purpose: Creates a mapping of rgb colors to "css colors"
* Inputs: List of css colors
* Outputs: Dictionary of rgbs to css colors

#####`reduce_to_requested_color_space(self, pix_obj, im, color_mapping)`
* Purpose: Creates an image in which colors are changed to be whatever they are closest to from a list of colors
* Inputs: PIL pixel object, image, dictionary of rgbs to css colors
* Outputs: Color-simplified image

-------------------

###synesthesizer.py
* The main attraction: Takes the image and makes its colors words. Works at the command line as well as through the web GUI powered by synserver.py
* Dependencies: pillow, webcolors, pygame, cooccurrence.py, and imagesimpler.py

####`Synesthesizer()`:
#####`combinatorics(self)`
* Purpose: Creates a file containing a pickled dictionary, keyed by color words, of strings containing associates that are up to 25 characters long
* Inputs: None
* Outputs: Nothing explicit

#####`reconstitute(self)`
* Purpose: Unpickles the dictionary created by `combinatorics()` and saves it as an attribue of the `Synesthesizer`
* Inputs: None
* Outputs: Nothing explicit

#####`synesthesize(self, image, colors, fontname)`
* Purpose: Take an image, replace all the colors with words associated with the colors, saves the image to disk
* Inputs: Image to be adulterated, colors to be used
* Outputs: Filename of created image

* Contains three helper methods: `check_fit()`, `get_space()`, and `paint_picture()` 
