# -*- coding: utf-8 -*-
#
# 14.11.19
# J.rugis
#

import matplotlib.pyplot as plt
import numpy as np

import oiffile as oi
    
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
#fname += 'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-002.oib'
#fname += 'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-004-Zoom.oib'
#fname += 'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-006-Zoom.oib'
#fname += 'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-007-Zoom.oib'
fname += 'Rb NaK ATPase1-500-500 + Ms ZO-1 1-250-500-008-Zoom.oib'
F = oi.imread(fname)                                  # comes in as uint16
F = np.transpose(F,(1,2,3,0)).astype(float) / (2**16) # convert to float 0.0 - 1.0

A1 = F.copy() 
A1[:,:,:,2] = 0.0 # clear the third channel, leaving red and green
A1 /= A1.max()    # normalize all to 1.0
A1 *= 10.0        # brighten
figA1, axA1 = plt.subplots(1, 1)
trackerA1 = IndexTracker(axA1, A1)
figA1.canvas.mpl_connect('scroll_event', trackerA1.onscroll)

A2 = F.copy()
A2[:,:,:,0] = A2[:,:,:,2] # duplicate the third channel
A2[:,:,:,1] = A2[:,:,:,2] #  ...
A2 /= A2.max()            # normalize all to 1.0
figA2, axA2 = plt.subplots(1, 1)
trackerA2 = IndexTracker(axA2, A2)
figA2.canvas.mpl_connect('scroll_event', trackerA2.onscroll)


plt.show()

#cv2.imshow("opencv image", B[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()