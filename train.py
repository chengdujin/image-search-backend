#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
from numpy import *
import os
import sift
import sys

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)


def hist_similar(img):
    return img.histogram()

def sift_similar(img):
    img.save('./tmp/reg_img.jpg')
    key = sift.process_image('./tmp/reg_img.jpg')
    l, d = sift.read_features(key)
    return ravel(d)

def extract_features(name, img):
    #feature = hist_similar(img)
    feature = sift_similar(img).tolist()
    rclient.set(feature, name)

def make_regalur_image(img, size = (256, 256)):
    return img.resize(size).convert('L')

def calculate_features(name, path, img):
    regular = make_regalur_image(Image.open('%s/%s' % (path, img)))
    #regular = Image.open('%s/%s' % (path, img)).convert('L')
    extract_features(name, regular)
    return '%s/%s is processed!' % (path, img)	

if __name__ == '__main__':
    name = sys.argv[1]
    path = sys.argv[2]
    for f in os.listdir(path):
        print 'processing %s ...' % f
        print calculate_features(name, path, f)
