# -*- coding: utf-8 -*-
#
# 14.11.19
# J.rugis
#

import matplotlib.pyplot as plt
import numpy as np
import oiffile as oif
from skimage import exposure
from skimage.util import img_as_float
#from skimage.util import img_as_ubyte
    
class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.X = X
        self.slices, rows, cols, colors = self.X.shape
        self.ind = 0
        self.im = ax.imshow(self.X[self.ind, :, :, :])
        self.update()
    def onscroll(self, event):
        #print("%s %s" % (event.button, event.step))
        if event.button == 'down':
            if self.ind < self.slices - 1 : self.ind = (self.ind + 1)
        else:
            if self.ind > 0 : self.ind = (self.ind - 1)
        self.update()
    def update(self):
        self.im.set_data(self.X[self.ind, :, :, :])
        self.ax.set_ylabel('slice %s' % (self.ind + 1))
        self.im.axes.figure.canvas.draw()


# get an image stack
fname = '/Users/jrug001/Desktop/nesi00119/mesh-cells/images/nak_atpase_zo1/'
LIST = ['Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-002.oib',
        'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-004-Zoom.oib',
        'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-006-Zoom.oib',
        'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-007-Zoom.oib',
        'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-008-Zoom.oib']
fname += LIST[4]
F = img_as_float(np.transpose(oif.imread(fname),(1,2,3,0))) # rearrange columns

RG = exposure.rescale_intensity([1.0 ,1.0, 0.0] * F.copy(), in_range=(0.001, 0.01))
figA1, axA1 = plt.subplots(1, 1)
trackerA1 = IndexTracker(axA1, RG)
figA1.canvas.mpl_connect('scroll_event', trackerA1.onscroll)

P = F.copy()
P[:,:,:,0] = P[:,:,:,2]  # duplicate the optical channel 
P[:,:,:,1] = P[:,:,:,2]  # ...
P = exposure.rescale_intensity(P)
figA2, axA2 = plt.subplots(1, 1)
trackerA2 = IndexTracker(axA2, P)
figA2.canvas.mpl_connect('scroll_event', trackerA2.onscroll)

plt.show()

#cv2.imshow("opencv image", B[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()