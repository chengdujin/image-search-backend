# http://ascratchpad.blogspot.jp/2010/06/siftpy-python-sift-siftpp.html

from PIL import Image
from PILNumpyConverter import *
from siftpy import *
from numpy import *
import cv

captured =  cv.CaptureFromFile('/home/ubuntu/playground/img1.jpg')
frame = cv.QueryFrame(captured)
gray = cv.CreateImage((frame.width, frame.height), 8, 1)
cv.CvtColor(frame, gray, cv.CV_BGR2GRAY)

# scale input image for faster processing
__scale__ = 2
small_img = cv.CreateImage((cv.Round(frame.width/__scale__), cv.Round(frame.height/__scale__)), 8, 1)
cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
cv.EqualizeHist(small_img, small_img)

pi = Image.fromstring("L", cv.GetSize(small_img), small_img.tostring())         
a = image2array(pi)
print a
print '+++++++++++++'
b = ravel(a)
print b
s_res = sift(a)
#print '/////////////'
#print s_res
#n_res = array(s_res)
#print n_res
