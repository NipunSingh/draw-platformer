# USAGE
# python image_processing_visualization.py --image images/page.jpg 

from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filters import threshold_adaptive
from skimage.transform import pyramid_reduce
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(image, (5, 5), 0)

edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print "STEP 1: Edge Detection"
cv2.imshow("Image", image)
#cv2.imshow("Edged", edged)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
# (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

# show the contour (outline) of the piece of paper
print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
cv2.imshow("Color Wrapped", imutils.resize(warped, height = 650))
cv2.waitKey(0)


resized_image = imutils.resize(warped, height= 650);

hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([100,50,50])
upper_blue = np.array([140,255,255])
 # Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)
# Bitwise-AND mask and original image
blue_res = cv2.bitwise_and(hsv, hsv, mask= mask)
cv2.imshow("Blue Image", blue_res)
cv2.waitKey(0)


red = np.uint8([[[0, 0, 255]]])
hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV) # (0,255,255)

lower_red = np.array([0,50,50]) # also parses as red
upper_red = np.array([25,255,255]) #also parses as red
 # Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_red, upper_red)
# Bitwise-AND mask and original image
red_res = cv2.bitwise_and(hsv, hsv, mask= mask)
cv2.imshow("Red Image", red_res)
cv2.waitKey(0)


#new_lower_red = np.array([160,50,50]) # also parses as red
#new_upper_red = np.array([180,255,255]) #also parses as red
 # Threshold the HSV image to get only blue colors
#new_red_mask = cv2.inRange(hsv, lower_red, upper_red)
#combined_mask = cv2.bitwise_or(mask, new_red_mask)
# Bitwise-AND mask and original image
#new_red_res = cv2.bitwise_and(hsv, hsv, mask= combined_mask)
#cv2.imshow("Red Try 2 Image", red_res)
#cv2.waitKey(0)

green = np.uint8([[[0, 255, 0]]])
hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
hsv_green # (60, 255, 255)

lower_green = np.array([40,30,30])
upper_green = np.array([85,255,255])
mask = cv2.inRange(hsv, lower_green, upper_green)
green_res = cv2.bitwise_and(hsv, hsv, mask= mask)
cv2.imshow("Green Image", green_res)
cv2.waitKey(0)


lower_pink = np.array([140,30,30])
upper_pink = np.array([175,255,255])
mask = cv2.inRange(hsv, lower_pink, upper_pink)
pink_res = cv2.bitwise_and(hsv, hsv, mask= mask)
cv2.imshow("Pink Image", pink_res)
cv2.waitKey(0)


# Black Image
black_image = hsv.copy()
nrows = hsv.shape[0]
ncols = hsv.shape[1]
for i in range(nrows):
	for j in range(ncols):
		if (hsv[i][j][2] < 125):
			black_image[i][j] = [0,0,0] #set black
		else:
			black_image[i][j] = [0,0,255] #set white

cv2.imshow("Black Image", black_image)
cv2.waitKey(0)



# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 251, offset = 10)
warped = warped.astype("uint8") * 255


nrows = warped.shape[0]
ncols = warped.shape[1]
threshold_colors = np.zeros((nrows, ncols))

# switched rows / cols
for i in range(nrows):
	for j in range(ncols):
		if (warped[i][j] == 255): #background
			threshold_colors[i][j] = 1 #empty block
		else:
			if (green_res[i][j][2] > 3):
				threshold_colors[i][j] = 12
			elif (black_image[i][j][2] == 0): #black
				threshold_colors[i][j] = 2
			elif (red_res[i][j][2] > 3):
				threshold_colors[i][j] = 9
			elif (blue_res[i][j][2] > 3):
				threshold_colors[i][j] = 8

			elif (pink_res[i][j][2] > 5):
				threshold_colors[i][j] = 5 #pink
			else:
				threshold_colors[i][j] = 2


#rotated_image = np.rot90(threshold_colors, k=3)
rotated_image = threshold_colors

cv2.waitKey(0)

# 650 / 44 = 14.77, 498 / 36 = 13.8333
import operator
def translate_image(img, output_width, output_height): # (img, width=44, height=36)
	result = np.zeros((output_height, output_width))
	nrows = img.shape[0] # 498
	ncols = img.shape[1] # 650
	row_size = nrows / output_height #498 / 36 = 13.8333
	col_size = ncols / output_width # 650 / 44 = 14.77
	for outter_i in range(0,output_height):
		for outter_j in range(0, output_width):
			votes = {1: 0, 12: 0, 9: 0, 8: 0, 5: 0, 2:0}
			for inner_i in range(outter_i* row_size, outter_i*row_size + row_size):
				for inner_j in range(outter_j*col_size, outter_j*col_size + col_size):
					if (inner_i < nrows and inner_j < ncols):
						color = img[inner_i][inner_j]
						votes[color] += 1
					best_color = max(votes.iteritems(), key=operator.itemgetter(1))[0]
					if (best_color == 1 and (votes[1] < (0.7 *row_size * col_size))):
						votes[1] = 0
						best_color = max(votes.iteritems(), key=operator.itemgetter(1))[0]
			result[outter_i][outter_j] = best_color
	return result

resized_image = translate_image(rotated_image, 44, 36)

# downsample
#resized_image = cv2.resize(rotated_image, (44,36))
np.set_printoptions(threshold=np.nan)
rounded_image = np.rint(resized_image).astype(int)


def eliminate_dups(img):
	nrows = img.shape[0]
	ncols = img.shape[1]

	def suppress_neighbhor(img, i, j, value):
		if i - 1 > 0:
			if (img[i - 1][j] == value):
				img[i - 1][j] = 1
		if i + 1 < nrows :
			if (img[i + 1][j] == value):
				img[i + 1][j] = 1
		if j - 1 > 0:
			if (img[i][j-1] == value):
				img[i][j-1] = 1
		if j + 1 < ncols:
			if (img[i][j + 1] == value):
				img[i][j + 1] = 1

	for i in range(nrows):
		for j in range(ncols):
			if (img[i][j] == 12):
				suppress_neighbhor(img, i, j, 12)
			elif (img[i][j] == 8):
				suppress_neighbhor(img, i, j, 8)

eliminate_dups(rounded_image)

def add_border(img):
	nrows = img.shape[0]
	ncols = img.shape[1]
	for j in range(ncols):
		img[nrows-1][j] = 2
	for i in range(nrows):
		img[i][0] = 2
		img[i][ncols-1] = 2

add_border(rounded_image)

import json
print json.dumps(rounded_image.tolist()) #used by the JS game engine to create a map 


# show the original and scanned images
print "STEP 3: Apply perspective transform"
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
