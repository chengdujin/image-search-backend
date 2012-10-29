#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import sift
from numpy import *

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)

from collections import OrderedList


def sift_similar(ls):
	ls.save('./tmp/ls.jpg')

	lkey = sift.process_image('./tmp/ls.jpg')
	ll, dl = sift.read_features(lkey)

	return ravel(dr)

def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	
	assert w % pw == h % ph == 0
	
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in xrange(0, w, pw) \
				for j in xrange(0, h, ph)]

def calc_similar(li, ri):
	for i, l in enumerate(split_image(li)):
		rclient.hset('hillary_clinton', i, sift_similar(l))

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def calc_similar_by_path(lf):
	li = make_regalur_image(Image.open(lf))
	return calc_similar(li)	

if __name__ == '__main__':
    import sys
    print calc_similar_by_path(sys.argv[1])