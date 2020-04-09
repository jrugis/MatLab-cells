# -*- coding: utf-8 -*-
#
# 09.04.20
# J.rugis
#

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-3_0002.oir"

# get the image stack
#os.system("/Users/jrug001/Desktop/nesi00119/bftools/bfconvert " + filename + " temp.tiff")
A0 = io.imread('temp.tiff')
#os.system("rm temp.tiff")
print(A0.shape)
print(type(A0[0,0,0]))
print(np.min(A0), np.max(A0))
print(np.count_nonzero(A0 == np.max(A0)))

B = np.where(A0 == np.max(A0))
print(B)

A = A0[:, 325, 62]
plt.figure(1)
P0 = plt.plot(A)

plt.show()
