""" 
Python module for use with David Lowe's SIFT code available at:
http://www.cs.ubc.ca/~lowe/keypoints/
adapted from the matlab code examples.

http://www.janeriksolem.net/2009/02/sift-python-implementation.html
Jan Erik Solem, 2009-01-30
"""

import os
import subprocess
from numpy import *
import pylab


def process_image(imagename):
    """ process an image and save the results in a .key ascii file"""
    p = subprocess.Popen(args="/var/www/wsgi/bin/jpegtopnm %s | /var/www/wsgi/bin/ppmtopgm | /var/www/wsgi/bin/sift" % imagename, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    #p.wait()
    output =  p.stdout.read()
    # print '%s processed ...' % imagename
    return output
    
def read_features(key):
    """ read feature properties and return in matrix form"""
    whole = str(key).partition('\n')
    header = whole[0].split()

    num = int(header[0]) #the number of features
    featlength = int(header[1]) #the length of the descriptor
    if featlength != 128: #should be 128 in this case
        raise RuntimeError, 'Keypoint descriptor length invalid (should be 128).' 
        
    locs = zeros((num, 4))
    descriptors = zeros((num, featlength));        

    # print 'header computed ...'
    #parse the .key file
    e = whole[2].split()   
    pos = 0
    for point in range(num):
        #row, col, scale, orientation of each feature
        for i in range(4):
            locs[point,i] = float(e[pos+i])
        pos += 4
        
        #the descriptor values of each feature
        for i in range(featlength):
            descriptors[point,i] = int(e[pos+i])
        #print descriptors[point]
        pos += 128
        
        #normalize each input vector to unit length
        descriptors[point] = descriptors[point] / linalg.norm(descriptors[point])
        #print descriptors[point]

    # print 'body computed ...'
    return locs,descriptors
    
def match(desc1,desc2):
    """ for each descriptor in the first image, select its match to second image
        input: desc1 (matrix with descriptors for first image), 
        desc2 (same for second image)"""
    
    dist_ratio = 0.6
    desc1_size = desc1.shape
    
    matchscores = zeros((desc1_size[0],1))
    desc2t = desc2.T #precompute matrix transpose
    for i in range(desc1_size[0]):
        dotprods = dot(desc1[i,:],desc2t) #vector of dot products
        dotprods = 0.9999*dotprods
        #inverse cosine and sort, return index for features in second image
        indx = argsort(arccos(dotprods))
        
        #check if nearest neighbor has angle less than dist_ratio times 2nd
        if arccos(dotprods)[indx[0]] < dist_ratio * arccos(dotprods)[indx[1]]:
            matchscores[i] = indx[0]
        
    return matchscores 
    
def match2(desc1,desc2):
    """ for each descriptor in the first image, 
        select its match in the second image.
        input: desc1 (descriptors for the first image), 
        desc2 (same for second image). """
    
    desc1 = array([d/linalg.norm(d) for d in desc1])
    desc2 = array([d/linalg.norm(d) for d in desc2])
    
    dist_ratio = 0.6
    desc1_size = desc1.shape
    
    matchscores = zeros((desc1_size[0],1))
    desc2t = desc2.T #precompute matrix transpose
    for i in range(desc1_size[0]):
        dotprods = dot(desc1[i,:],desc2t) #vector of dot products
        dotprods = 0.9999*dotprods
        #inverse cosine and sort, return index for features in second image
        indx = argsort(arccos(dotprods))
        
        #check if nearest neighbor has angle less than dist_ratio times 2nd
        if arccos(dotprods)[indx[0]] < dist_ratio * arccos(dotprods)[indx[1]]:
            matchscores[i] = int(indx[0])
    
    return matchscores

def match_twosided(desc1,desc2):
    """ two-sided symmetric version of match(). """
    
    matches_12 = match2(desc1,desc2)
    matches_21 = match2(desc2,desc1)
    
    ndx_12 = matches_12.nonzero()[0]
    
    #remove matches that are not symmetric
    for n in ndx_12:
        if matches_21[int(matches_12[n])] != n:
            matches_12[n] = 0 
    
    return matches_12

def plot_features(im,locs):
    """ show image with features. input: im (image as array), 
        locs (row, col, scale, orientation of each feature) """
    
    pylab.gray()
    pylab.imshow(im)
    pylab.plot([p[1] for p in locs], [p[0] for p in locs], 'ob')
    pylab.axis('off')
    pylab.show()
    
def appendimages(im1,im2):
    """ return a new image that appends the two images side-by-side."""
    
    #select the image with the fewest rows and fill in enough empty rows
    rows1 = im1.shape[0]    
    rows2 = im2.shape[0]
    
    if rows1 < rows2:
        im1 = concatenate((im1,zeros((rows2-rows1,im1.shape[1]))), axis=0)
    else:
        im2 = concatenate((im2,zeros((rows1-rows2,im2.shape[1]))), axis=0)
        
    return concatenate((im1,im2), axis=1)
    
def plot_matches(im1,im2,locs1,locs2,matchscores):
    """ show a figure with lines joining the accepted matches in im1 and im2
        input: im1,im2 (images as arrays), locs1,locs2 (location of features), 
        matchscores (as output from 'match'). """
    
    im3 = appendimages(im1,im2)

    pylab.gray()
    pylab.imshow(im3)
    
    cols1 = im1.shape[1]
    for i in range(len(matchscores)):
        if matchscores[i] > 0:
            pylab.plot([locs1[i,1], locs2[int(matchscores[i]),1]+cols1], [locs1[i,0], locs2[int(matchscores[i]),0]], 'c')
    pylab.axis('off')
    pylab.show()

