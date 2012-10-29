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
    lh = lh.histogram()
    rh = eval(rh)

    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def sift_similar(limg, rimg):
    limg.save('./tmp/reg_limg.jpg')
    lkey = sift.process_image('./tmp/reg_limg.jpg')
    ll, dl = sift.read_features(lkey)

    zipped = zip(ravel(dl), array(eval(rimg)))
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def calculate_similarity(limg, rimg):
    regular_limg = make_regalur_image(Image.open(limg))
    #return sift_similar(regular_limg, rimg)
    return hist_similar(regular_limg, rimg)

if __name__ == '__main__':
    max_score = 0
    max_key = None

    keys = rclient.keys()
    for key in keys:
        current_score = calculate_similarity(sys.argv[1], key)
        if current_score > max_score:
            max_score = current_score
            max_key = key
            print max_score
    print 'final: %s' % rclient.get(key)
