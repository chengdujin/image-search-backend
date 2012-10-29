#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
from numpy import *
import sift
import sys

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)


def sift_similar(limg, rimg):
    limg.save('./tmp/reg_limg.jpg')
    lkey = sift.process_image('./tmp/reg_limg.jpg')
    ll, dl = sift.read_features(lkey)

    zipped = zip(ravel(dl), array(rimg))
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))

	zipped = zip(ravel(dl), ravel(dr))
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def calculate_similarity(limg, rimg):
    regular_limg = make_regalur_image(Image.open(limg))
    # return hist_similar(li.histogram(), ri.histogram())
	# return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0
    return sift_similar(regular_limg, rimg)

if __name__ == '__main__':
    keys = rclient.keys()
    for key in keys:
        current = calculate_similarity(sys.argv[1], key)
        if current > max:
            max = current
    print max
