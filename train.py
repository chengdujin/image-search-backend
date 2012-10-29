#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
from numpy import *
import sift
import sys

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)


def sift_similar(img):
	img.save('./tmp/reg_img.jpg')
	key = sift.process_image('./tmp/reg_img.jpg')
	l, d = sift.read_features(key)
	return ravel(d)

def extract_features(img, index):
	rclient.hset('hillary_clinton', index, sift_similar(img))

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def calculate_features(path, img):
	regular = make_regalur_image(Image.open('%s%s' % (path, img)))
	extract_features(regular, img)
    return '%s%s is processed!' % (path, img)	

if __name__ == '__main__':
    path = sys.argv[1]
    for f in os.list(path):
        calculate_features(path, f)
