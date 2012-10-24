import Image
import webcolors
import math


class ImageSimpler():
	"""
	Purpose: To take an image and "round" all colors to one of a specified list of colors and then write out the mutated image
	Inputs: image to be manipulated, colors to be "rounded to", scaled size of the image
	Outputs: Nothing really
	"""

	def simplify(self, imagefile, colors, percentsize):
		image = Image.open(imagefile)

		if percentsize is not 100:
			newx = int(image.size[0]*(percentsize/100.00))
			newy = int(image.size[1]*(percentsize/100.00))
			image = image.resize((newx, newy))

		#mapping of rgb values to requested color words
		rgbsToColors = {}
		for color in colors:
			rgbsToColors[webcolors.name_to_rgb(color)] = color

		#makes the image more readily mutable and readable by creating a "Pixel Access Object"
		pixels = image.load()
		
		#matching pixels to their closest specified color
		for x in range(image.size[0]):
			for y in range(image.size[1]):
				pix = pixels[x,y]
				closest = None
				mindist = float('Inf')
				#find which rgb triplet is the closest through Euclidean distance of their vectors
				for rgb in rgbsToColors:
					dist = math.sqrt((rgb[0]-pix[0])*(rgb[0]-pix[0])+(rgb[1]-pix[1])*(rgb[1]-pix[1])+(rgb[2]-pix[2])*(rgb[2]-pix[2]))
					if dist < mindist:
						mindist = dist
						closest = rgb
				pixels[x,y] = closest

		image.show()


if __name__ == '__main__':
	iSimp = ImageSimpler()
	iSimp.simplify('../lime-cat.jpg', ['green','red', 'yellow', 'white', 'black', 'orange'], 50)