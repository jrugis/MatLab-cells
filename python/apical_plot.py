# -*- coding: utf-8 -*-
#
# 07.04.20
# J.rugis
#

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import exposure
from skimage.util import img_as_float32

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-3_0002.oir"
filemask= "apical_mask.tif"

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# get the image stack
#os.system("/Users/jrug001/Desktop/nesi00119/bftools/bfconvert " + filename + " temp.tiff")
A0 = img_as_float32(io.imread('temp.tiff'))
A0 = exposure.rescale_intensity(A0)
#os.system("rm temp.tiff")

# average out y-direction aliasing over every other line
#for n in range(A0.shape[0] - 1): # average over every two lines
#  A0[n] = (A0[n] + A0[n+1]) / 2.0

# get the apical mask
M = io.imread(filemask)
N, counts = np.unique(M, return_counts=True)
print(N[1:])
print(counts[1:])
plt.figure(0)
plt.imshow(M, cmap='gray')

for n in N:
  if(n==0):
    continue
  A = A0[:, M==N[n]]
  B = np.sum(A, axis=1) / A.shape[1]
  plt.figure(n)
  P0 = plt.plot(A)
  P1 = plt.plot(B, color='black')

plt.show()
