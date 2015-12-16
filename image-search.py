#!/usr/bin/python
#
#
# image-search.py
''' This program will search a database of images and find the matching 
ones from a sourced image.'''

from PIL import Image
import imagehash
import argparse
import shelve


def ham_dist(str1, str2):
    assert len(str1) == len(str2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "path to dataset of images")
ap.add_argument("-s", "--shelve", required = True,
    help = "output shelve database")
ap.add_argument("-q", "--query", required = True,
    help = "path to the query image")
args = vars(ap.parse_args())
print(type(args["shelve"]))

# open the shelve database
db = shelve.open(args["shelve"])

# load the query image, compute the difference image hash, and
# and grab the images from the database that have the same hash
# value
filenames=[]
query = Image.open(args["query"])
h = str(imagehash.dhash(query))
for ihash in db:
    hd = ham_dist(h, ihash)
    # print(hd)
    if hd < 12:
        filenames.append(str(db[ihash]).strip("[]'"))

print ("Found %d images" % (len(filenames)))

# loop over the images
for filename in filenames:
    image = Image.open(args["dataset"] + "/" + str(filename))
    image.show()
    
# close the shelve database
db.close()
