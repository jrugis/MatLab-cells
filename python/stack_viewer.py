# -*- coding: utf-8 -*-
#
# 14.11.19
# J.rugis
#

import matplotlib.pyplot as plt

import stack_utils as su
    
class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.X = X
        self.slices, rows, cols = self.X.shape
        self.ind = 0
        self.im = ax.imshow(self.X[self.ind, :, :], cmap='gray')
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
A = su.get_stack('stack.tif')

# display the image stack A
figA, axA = plt.subplots(1, 1)
trackerA = IndexTracker(axA, A)
figA.canvas.mpl_connect('scroll_event', trackerA.onscroll)

plt.show()

#cv2.imshow("opencv image", B[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()