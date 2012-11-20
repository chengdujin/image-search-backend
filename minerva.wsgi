#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves as the main entrance
# to minerva
#
# @author Yuan Jin
# @created Oct. 27, 2012
# @updated Oct. 29, 2012
#


import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import cgi
from collections import OrderedDict
import string
import tesseract
import threading

import Queue
queue = Queue.Queue()


class OcrThread(threading.Thread):
    def __init__(self, api, queue):
        threading.Thread.__init__(self)
        self.api = api
        self.queue = queue

    def run(self):
        while True:
            image_number = self.queue.get()
            image = screenshots[image_number]
            screenshots[image_number] = tesseract.ProcessPagesBuffer(image, len(image), self.api)
            self.queue.task_done()

def ocr(language):
    # thread pool
    api = tesseract.TessBaseAPI()
    api.Init(".", language, tesseract.OEM_DEFAULT)

    # determine number of threads to work on the images
    number_of_tasks = len(screenshots)
    number_of_threads = 5 if number_of_tasks > 5 else number_of_tasks

    for t in xrange(number_of_threads):
        ot = OcrThread(api, queue)
        ot.setDaemon(True)
        ot.start()
    queue.join()

    return ' '.join([x for x in reversed(screenshots.values())])

def read_http(environ):
    'read binary image file and write to local disk'
    global screenshots
    screenshots = OrderedDict()
    # default language 
    language = 'eng'

    bin_data = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    for key in bin_data.keys():
        if key == 'Language type':
            language = bin_data[key].value
        else:
            screenshots['%s' % key] = bin_data[key].value
            queue.put('%s' % key)

    return language

def application(environ, start_response):
    try:
        language = read_http(environ)
        output = ocr(language)

        if output is None:
            raise Exception('Void output!')
        header = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]

        start_response("200 OK", header)
        return [output]
    except Exception, e:
        header = [('Content-type', 'text/plain'), ('Content-Length', str(len(str(e))))]
        start_response("200 OK", header)
        return [str(e)]
