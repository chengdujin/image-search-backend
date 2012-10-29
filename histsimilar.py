#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import sift
from numpy import *

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	
	assert w % pw == h % ph == 0
	
	return [img.crop((i, j, i+pw, j+ph)).copy() \
				for i in xrange(0, w, pw) \
				for j in xrange(0, h, ph)]

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))

def sift_similar(ls, rs):
	ls.save('./tmp/ls.jpg')
	rs.save('./tmp/rs.jpg')

	lkey = sift.process_image('./tmp/ls.jpg')
	ll, dl = sift.read_features(lkey)

	rkey = sift.process_image('./tmp/rs.jpg')
	lr, dr = sift.read_features(rkey)

	print ravel(dr)
	zipped = zip(ravel(dl), ravel(dr))
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def calc_similar(li, ri):
#	return hist_similar(li.histogram(), ri.histogram())
	# return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0
	return sum(sift_similar(l, r) for l, r in zip(split_image(li), split_image(ri))) / 16.0
			

def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)	

if __name__ == '__main__':
    import sys
    print calc_similar_by_path(sys.argv[1], sys.argv[2])