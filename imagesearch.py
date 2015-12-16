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

def imageSearch(dataset, shlv, query):
    # open the shelve database
    db = shelve.open(shlv)

    # load the query image, compute the difference image hash, and
    # and grab the images from the database that have the same hash
    # value
    filenames=[]
    q = Image.open(query)
    h = str(imagehash.dhash(q))
    for ihash in db:
        hd = ham_dist(h, ihash)
        # print(hd)
        if hd < 12:
            filenames.append(str(db[ihash]).strip("[]'"))

    print ("Found %d images" % (len(filenames)))

    # loop over the images
    # for filename in filenames:
    #     image = Image.open(dataset + "/" + str(filename))
    #     image.show()
    return (filenames)    
    # close the shelve database
    db.close()

# Main test
# img = str("images")
# ds = str("patterns")
# q = str("sample2.jpg")
# imageSearch(img,ds,q)