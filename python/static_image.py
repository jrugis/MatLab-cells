# -*- coding: utf-8 -*-
#
# 06.04.20
# J.rugis
#

import os
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage import exposure
from skimage.util import img_as_float32

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-3_0003.oir"

# get the image stack
os.system("/Users/jrug001/Desktop/nesi00119/bftools/bfconvert " + filename + " temp.tiff")
A = img_as_float32(exposure.rescale_intensity(io.imread('temp.tiff')))
os.system("rm temp.tiff")

A = np.concatenate((A[:100,:,:], A[249:,:,:])) # unstimulated only
A = exposure.rescale_intensity(A)
M = np.zeros(A[0].shape)
for n in range(A.shape[0]): # average over time
  M += A[n]
M /= A.shape[0]

for n in range(M.shape[0] - 1): # average over every two lines
  M[n] = (M[n] + M[n+1]) / 2.0

io.imsave("test.png", M)

plt.imshow(M, cmap='gray')
plt.show()
