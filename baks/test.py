from PIL import Image
from numpy import *
from pylab import *
import sift

# print full array
set_printoptions(threshold=nan)

key1 = sift.process_image('h3.jpg')
#print key
#nk = str(key).split('\n')
#print len(nk)

l1, d1 = sift.read_features(key1)
img1 = array(Image.open('h3.pgm'))
print 'got the first pic'
#print d
#print array(ravel(d1))
#print '================================================'
sift.plot_features(img1, l1)

key2 = sift.process_image('h4.jpg')
l2, d2 = sift.read_features(key2)
img2 = array(Image.open('h4.pgm'))
print 'got the second pic'
sift.plot_features(img2, l2)
#print d2
#print array(ravel(d2))
#print '================================================'

'''
key3 = sift.process_image('img3.jpg')
l3, d3 = sift.read_features(key3)
img3 = array(Image.open('img3.pgm'))
#print d3
#print array(ravel(d3))
'''

m = sift.match_twosided(d1, d2)
print m
figure()
sift.plot_matches(img1, img2, l1, l2, m)
