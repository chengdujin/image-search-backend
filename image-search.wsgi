#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
sys.path.append('/var/www/wsgi')

import cgi
import Image
from numpy import *
import sift
import time
import threading

import redis
REDIS_SERVER = '127.0.0.1'
rclient = redis.StrictRedis(REDIS_SERVER)

import Queue
queue = Queue.Queue()

def find_max():
    key = keys[records[max(records.keys())]]
    return rclient.get(key)

def hist_similar(lh, rh):
    rh = eval(rh)
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def sift_similar(limg, rimg):
    zipped = zip(limg, array(eval(rimg)))
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zipped)

def calculate_similarity(limg, rimg):
    return hist_similar(limg, rimg)
    #return sift_similar(limg, rimg)

class ImageSearchThread(threading.Thread):
    def __init__(self, request_features):
        threading.Thread.__init__(self)
        self.request_features = request_features

    def run(self):
        while True:
            feature_number = queue.get()
            a = time.time()
            trained_feature = keys[feature_number]
            score = calculate_similarity(self.request_features, trained_feature)
            records[score] = feature_number
            b = time.time()
            #print 'feature %s processed in %f seconds' % (feature_number, b-a)
            queue.task_done()

def image_search(request_features):
    global keys
    key = []
    keys = rclient.keys()
    global records
    records = {}
    total_keys = len(keys)

    number_of_threads = 1 
    for t in xrange(number_of_threads):
        ist = ImageSearchThread(request_features)
        #print '%s started ...' % str(ist)
        ist.setDaemon(True)
        ist.start()

    for n in xrange(total_keys):
        queue.put(n)
        records[n] = 0
    queue.join()
    return find_max()

def compute_histogram(limg):
    return limg.histogram()

def compute_sift(limg):
    limg.save('/var/www/wsgi/tmp/reg_limg.jpg')
    lkey = sift.process_image('/var/www/wsgi/tmp/reg_limg.jpg')
    ll, dl = sift.read_features(lkey)
    return ravel(dl)

def make_regalur_image(img, size = (256, 256)):
	return img.resize(size).convert('RGB')

def calculate_features(limg):
    regular_limg = make_regalur_image(Image.open(limg).convert('L'))
    return compute_histogram(regular_limg)
    #return compute_sift(regular_limg)

def read_http(environ):
    'read binary image file and write to local disk'
    image_path = ''
    bin_data = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    for key in bin_data.keys():
        image_path = '/var/www/wsgi/tmp/%s' % key
        f = open(image_path, 'wb')
        f.write(bin_data[key].value)
        f.close()
    return image_path

def application(environ, start_response):
    try:
        request_image = read_http(environ)
        request_features = calculate_features(request_image)
        output = image_search(request_features)

        if output is None:
            raise Exception('Void output!')
        header = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]

        start_response("200 OK", header)
        return [output]
    except Exception, e:
        header = [('Content-type', 'text/plain'), ('Content-Length', str(len(str(e))))]
        start_response("200 OK", header)
        return [str(e)]  
'''
if __name__ == '__main__':
    a = time.time()
    wanted = calculate_features(sys.argv[1]) 
    b = time.time()
    print 'calculating features takes ...', b - a 
    #output = image_search(wanted)
    #print output
    keys = rclient.keys()
    for key in keys:
        current = calculate_similarity(wanted, key)
    c = time.time()
    print c - b
'''
