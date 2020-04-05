# -*- coding: utf-8 -*-
#
# 08.11.19
# J.rugis
#

from cv2 import bilateralFilter
import numpy as np
import matplotlib.pyplot as plt
from skimage import io

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.X = X
        self.slices, rows, cols = X.shape
        self.ind = 0
        self.im = ax.imshow(self.X[self.ind, :, :],cmap='gray')
        self.update()
    def onscroll(self, event):
        #print("%s %s" % (event.button, event.step))
        if event.button == 'down':
            if self.ind < self.slices - 1 : self.ind = (self.ind + 1)
        else:
            if self.ind > 0 : self.ind = (self.ind - 1)
        self.update()
    def update(self):
        self.im.set_data(self.X[self.ind, :, :])
        self.ax.set_ylabel('slice %s' % (self.ind + 1))
        self.im.axes.figure.canvas.draw()

# get an image stack
A = io.imread('stack.tif')
B = np.copy(A)  # deep copy

# display the image stacks A and B
figA, axA = plt.subplots(1, 1)
trackerA = IndexTracker(axA, A)
figA.canvas.mpl_connect('scroll_event', trackerA.onscroll)

figB, axB = plt.subplots(1, 1)
trackerB = IndexTracker(axB, B)
figB.canvas.mpl_connect('scroll_event', trackerB.onscroll)

plt.show()

# modify image stack B
#cv2.blur(B[0],(5,5),B[0])              # process single slice
#[cv2.blur(x, (5,5), x) for x in B[:]]  # process whole stack
#[cv2.medianBlur(x, 5, x) for x in B[:]]  # process whole stack
#[cv2.GaussianBlur(x, (0,0), 5, x) for x in B[:]]  # process whole stack
#[cv2.bilateralFilter(x, 6, 12, 3, x) for x in B[:]]  # process whole stack
[bilateralFilter(A[i], 9, 200, 200, B[i]) for i in range(A.shape[0])]
#[cv2.morphologyEx(B[i], cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(10,10)),A[i]) for i in range(B.shape[0])]
trackerB.update()

io.imsave('stackB.tif', B)

#cv2.imshow("opencv image", B[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()