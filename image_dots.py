# -*- coding: utf-8 -*-
###############################################################################
#
# 08.11.19
# J.rugis
#
###############################################################################

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

from stack_utils import get_stack, save_stack, save_points
    
###############################################################################
# CLASSES AND FUNCTIONS
###############################################################################

class cTracker(object):
    def __init__(self, ax, A):
        ax.set_title('use scroll wheel to navigate images')
        self.ax = ax                               # plot axis
        self.A = A                                 # image stack data
        self.slices, rows, cols = A.shape
        self.lP = [[] for n in range(self.slices)] # list of circle center points
        self.lA = [[] for n in range(self.slices)] # list of artist circles to draw
        self.ind = 0                               # displayed stack frame
        self.im = ax.imshow(A[self.ind, :, :],cmap='gray')
        self.update()

    def add_point_artist(self, ind, x, y):
        self.lP[ind].append((x,y)); save_points('points.txt', self.lP)
        self.lA[ind].append(self.ax.add_artist(
                plt.Circle((x, y), 22, color=(1,1,0), lw=1, fill=False, picker=1)))

    def onscroll(self, event):  
        # stack scrolling
        #print("%s %s" % (event.button, event.step))
        [a.remove() for a in self.lA[self.ind]]
        if event.button == 'down':
            if self.ind < self.slices - 1 : self.ind = (self.ind + 1)
        else: 
            if self.ind > 0 : self.ind = (self.ind - 1)
        [self.ax.add_artist(a) for a in self.lA[self.ind]]
        self.update()

    def onpress(self, event):
        # adding circles
        if event.button is MouseButton.LEFT and event.inaxes:
            x = int(event.xdata)
            y = int(event.ydata)
            self.add_point_artist(self.ind, x, y)
            self.im.axes.figure.canvas.draw()

    def onpick(self, event):
        # deleting circles
        if event.mouseevent.button is MouseButton.RIGHT:
            i = self.lA[self.ind].index(event.artist)
            self.lP[self.ind].pop(i); save_points('points.txt', self.lP)
            self.lA[self.ind].pop(i)
            event.artist.remove()
            self.im.axes.figure.canvas.draw()

    def update(self):
        self.im.set_data(self.A[self.ind, :,:])
        self.ax.set_ylabel('slice %s' % (self.ind + 1))
        self.im.axes.figure.canvas.draw()

###############################################################################
# MAIN PROGRAM
###############################################################################

#### get an image stack
A = get_stack('./images/ImageSequence8bit/*.tif')
B = np.copy(A)  # deep copy

#### modify image stack
#cv2.blur(B[0],(5,5),B[0])                # process single slice
#[cv2.blur(x, (5,5), x) for x in B[:]]    # process whole stack
#[cv2.medianBlur(x, 5, x) for x in B[:]]  # process whole stack
#[cv2.GaussianBlur(x, (0,0), 5, x) for x in B[:]]     # process whole stack
#[cv2.bilateralFilter(x, 6, 12, 3, x) for x in B[:]]  # process whole stack
[cv2.bilateralFilter(A[i], 9, 200, 200, B[i]) for i in range(A.shape[0])]
#[cv2.morphologyEx(B[i], cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(10,10)),A[i]) for i in range(B.shape[0])]
save_stack('output.tif', B)

#### display the image stack B
fig, ax = plt.subplots(1, 1)
tracker = cTracker(ax, B)
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)      # for stack scrolling
fig.canvas.mpl_connect('button_press_event', tracker.onpress) # for adding circles
fig.canvas.mpl_connect('pick_event', tracker.onpick)          # for deleting circles

plt.show() # interactive GUI event loop

###############################################################################

