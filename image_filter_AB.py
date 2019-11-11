# -*- coding: utf-8 -*-
#
# 11.11.19
# J.rugis
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

from stack_utils import get_stack

class IndexTracker(object):
    def __init__(self, ax, X, Y):
        self.ax0 = ax[0]; self.ax1 = ax[1]
        ax[0].set_title('use scroll wheel to navigate images')
        self.X = X; self.Y = Y
        self.slices, rows, cols = X.shape
        self.ind = 0
        self.im0 = ax[0].imshow(self.X[self.ind, :, :],cmap='gray')
        self.im1 = ax[1].imshow(self.Y[self.ind, :, :],cmap='gray')
        self.update()
    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'down':
            if self.ind < self.slices - 1 : self.ind = (self.ind + 1)
        else:
            if self.ind > 0 : self.ind = (self.ind - 1)
        self.update()
    def update(self):
        self.im0.set_data(self.X[self.ind, :, :])
        self.im1.set_data(self.Y[self.ind, :, :])
        self.ax0.set_ylabel('slice %s' % (self.ind + 1))
        self.im0.axes.figure.canvas.draw()
        self.im1.axes.figure.canvas.draw()

# get an image stack
A = get_stack('./images/ImageSequence8bit/*.tif')
B = np.copy(A)  # deep copy

# display the image stacks A and B
fig, ax = plt.subplots(1, 2)
tracker = IndexTracker(ax, A, B)
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()

# modify image stack B
#cv2.blur(B[0],(5,5),B[0])              # process single slice
#[cv2.blur(x, (5,5), x) for x in B[:]]  # process whole stack
#[cv2.medianBlur(x, 5, x) for x in B[:]]  # process whole stack
#[cv2.GaussianBlur(x, (0,0), 5, x) for x in B[:]]  # process whole stack
#[cv2.bilateralFilter(x, 6, 12, 3, x) for x in B[:]]  # process whole stack
[cv2.bilateralFilter(A[i], 9, 200, 200, B[i]) for i in range(A.shape[0])]
#[cv2.morphologyEx(B[i], cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(10,10)),A[i]) for i in range(B.shape[0])]

tracker.update()
