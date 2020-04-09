# -*- coding: utf-8 -*-
#
# 06.04.20
# J.rugis
#

import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from skimage import io
from skimage import exposure
from skimage import filters
from skimage import feature
from skimage.util import img_as_float32
from skimage.morphology import binary_erosion
from skimage.morphology import binary_dilation
from skimage.morphology import label
from skimage.morphology import remove_small_objects
import cv2

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-3_0002.oir"

figX, ax = plt.subplots(1, 1) # an extra single figure

fig = plt.figure(figsize=(16, 4))
gs = gridspec.GridSpec(nrows=2, ncols=4, height_ratios=[1, 1])

# get the image stack
#os.system("/Users/jrug001/Desktop/nesi00119/bftools/bfconvert " + filename + " temp.tiff")
A0 = img_as_float32(io.imread('temp.tiff'))
A0 = exposure.rescale_intensity(A0)
#os.system("rm temp.tiff")

# average out y-direction aliasing over every other line
for n in range(A0.shape[0] - 1): # average over every two lines
  A0[n] = (A0[n] + A0[n+1]) / 2.0

###########################################
# unstimulated average over time
A = np.concatenate((A0[:100,:,:], A0[249:,:,:])) # unstimulated only
M = np.zeros(A[0].shape)
for n in range(A.shape[0]): # average over time
  M += A[n]
M /= A.shape[0]

# average out y-direction aliasing over every other line
for n in range(M.shape[0] - 1): # average over every two lines
  M[n] = (M[n] + M[n+1]) / 2.0

# plot image
ax0 = fig.add_subplot(gs[0, 0])
ax0.imshow(M, norm=None, cmap='coolwarm')

# plot image histogram
ax1 = fig.add_subplot(gs[1, 0])
ax1.hist(M.flatten(), bins=100)

###########################################
# stimulated average over time
A = A0[101:248,:,:] # stimulated only
N = np.zeros(A[0].shape)
for n in range(A.shape[0]): # average over time
  N += A[n]
N /= A.shape[0]

# average out y-direction aliasing over every other line
for n in range(N.shape[0] - 1): # average over every two lines
  N[n] = (N[n] + N[n+1]) / 2.0

# plot image
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(N, norm=None, cmap='coolwarm')

# plot image histogram
ax3 = fig.add_subplot(gs[1, 1])
ax3.hist(N.flatten(), bins=100)

###########################################
# difference: stimulated - unstimulated
O = N - M

# plot image
ax4 = fig.add_subplot(gs[0, 2])
ax4.imshow(O, norm=None, cmap='coolwarm')

# plot image histogram
ax5 = fig.add_subplot(gs[1, 2])
ax5.hist(O.flatten(), bins=100)

###########################################
# difference threashold
P = (O > 0.36).astype(float)

# plot image
ax6 = fig.add_subplot(gs[0, 3])
ax6.imshow(P, norm=None, cmap='gray')

###########################################
# remove small, thicken
Q = binary_erosion(P)
Q = binary_erosion(P)
Q = binary_erosion(P)
Q = remove_small_objects(Q, 16)
Q = binary_dilation(Q)
Q = binary_dilation(Q)
ax7 = fig.add_subplot(gs[1, 3])
ax7.imshow(Q, norm=None, cmap='gray')

# label
Q, n = label(Q, return_num=True)
print(n)
print(np.max(Q))

###########################################
#edge detection

#Q = filters.scharr(M)
#Q = filters.sobel(M)
#Q = filters.prewitt(M)
#Q = feature.canny(M, sigma=1.0)

###########################################
#im = cv2.imread("test.jpg")
#im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#v = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 2, 20, param1=25,param2=30,minRadius=2,maxRadius=8)
#print(v)
#circles = np.uint16(np.around(v))
#for i in circles[0,:]:
#  cv2.circle(M,(i[0],i[1]),i[2],(0,255,0),2) # draw the outer circle

###########################################
# show the plots
io.imsave("apical_mask.tif", Q)
ax.imshow(Q, norm=None, cmap='gray')
plt.tight_layout()
plt.show()


#for n in range(A.shape[0]): # average over time
#  inds = A[n] > M # find where image intensity > max intensity
#  M[inds] = A[n][inds] # update the maximum value at each pixel
#  inds = M < 0.002
#  N[inds] = 1.0
