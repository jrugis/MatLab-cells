#!/usr/bin/env python# -*- coding: utf-8 -*-
#
# 05.04.20
# J.rugis
#

import javabridge
import bioformats
from bioformats import log4j
import matplotlib.pyplot as plt
import numpy as np
import cv2

javabridge.start_vm(class_path=bioformats.JARS)
log4j.basic_config()

filename = "/Users/jrug001/Desktop/nesi00119/Yule/intravital/Mistgcamp-1.oir"

o = bioformats.OMEXML(bioformats.get_omexml_metadata(path=filename))

print()
print("####################################################")
print()
print(dir(o))
print()
print("image_count: ", o.image_count)

print()
print(dir(o.image()))
print()
print("acquisition date: ", o.image().AcquisitionDate)

print()
print(dir(o.image().Pixels))
print()
print("pixel type: ", o.image().Pixels.PixelType)
print("pixels: ", o.image().Pixels.SizeX, "x", o.image().Pixels.SizeY,  "x", o.image().Pixels.SizeZ)
print("channels: ", o.image().Pixels.SizeC)
print("time steps: ", o.image().Pixels.SizeT)
print("pixel physical size: ", o.image().Pixels.PhysicalSizeX, o.image().Pixels.PhysicalSizeXUnit, "x", o.image().Pixels.PhysicalSizeY, o.image().Pixels.PhysicalSizeYUnit)

print()
print("####################################################")
print()

#rd = bioformats.ImageReader(filename)
#im = np.zeros((o.image().Pixels.SizeT, o.image().Pixels.SizeX, o.image().Pixels.SizeY))
#for n in range(o.image().Pixels.SizeT):
#  print(n)
#  im[n] = bioformats.ImageReader(filename).read(c=0, t=n)
  
#print(im.max())

#cv2.blur(im[200],(5,5),im[200])

#plt.imshow(im, cmap='gray')
#plt.imshow(im[200], cmap='coolwarm')
#plt.show()

javabridge.kill_vm()
