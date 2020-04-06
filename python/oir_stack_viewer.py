# -*- coding: utf-8 -*-
#
# 05.04.20
# J.rugis
#

import os
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage import exposure
from skimage.util import img_as_float32
from cv2 import bilateralFilter

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-3_0002.oir"

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.X = X
        self.slices, rows, cols = self.X.shape
        self.ind = 150
        self.im = ax.imshow(self.X[self.ind, :, :], cmap='gray', norm=None, vmin=0.0, vmax=1.0)
        #self.im = ax.imshow(self.X[self.ind, :, :], cmap='coolwarm')
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

# get the image stack
#os.system("/Users/jrug001/Desktop/nesi00119/bftools/bfconvert " + filename + " temp.tiff")
A = img_as_float32(exposure.rescale_intensity(io.imread('temp.tiff'), in_range='uint10'))
#os.system("rm temp.tiff")

# filter and display histogram
B = np.copy(A)  # deep copy
#[bilateralFilter(A[i], 5, 200, 200, B[i]) for i in range(A.shape[0])]
P = plt.hist(B.flatten(), bins=30)

# display the image stack B
figA, axA = plt.subplots(1, 1)
trackerA = IndexTracker(axA, B)
figA.canvas.mpl_connect('scroll_event', trackerA.onscroll)

plt.show()
