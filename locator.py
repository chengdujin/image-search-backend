#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
from numpy import *
import sift
import sys

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)


def hist_similar(lh, rh):
    rh = eval(rh)
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def sift_similar(limg, rimg):
    zipped = zip(limg, array(eval(rimg)))
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def calculate_similarity(limg, rimg):
    #return hist_similar(limg, rimg)
    return sift_similar(limg, rimg)

def compute_histogram(limg):
    return limg.histogram()

def compute_sift(limg):
    limg.save('./tmp/reg_limg.jpg')
    lkey = sift.process_image('./tmp/reg_limg.jpg')
    ll, dl = sift.read_features(lkey)
    return ravel(dl)

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def calculate_features(limg):
    regular_limg = make_regalur_image(Image.open(limg))
    #return compute_histogram(regular_limg)
    return compute_sift(regular_limg)

if __name__ == '__main__':
    import time
    a = time.time()
    wanted = calculate_features(sys.argv[1]) 
    b = time.time()
    print 'calculating features takes ...', b - a
    max_score = 0
    max_key = None
    keys = rclient.keys()
    for key in keys:
        current_score = calculate_similarity(wanted, key)
        if current_score > max_score:
            max_score = current_score
            max_key = key
            print max_score, rclient.get(key)
    print 'final: %s' % rclient.get(max_key)
    c = time.time()
    print 'finding the best match takes ...', c - b
