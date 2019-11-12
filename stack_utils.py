# -*- coding: utf-8 -*-
#
# 08.11.19
# J.rugis
#

import glob
import numpy as np
from PIL import Image
import re

def get_stack(fname):
    filelist = glob.glob(fname);
    filelist.sort(key=lambda s: # numeric sort
        [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)])
    return np.array([np.array(Image.open(fname)) for fname in filelist])

def save_stack(fname, X):
    imlist = []
    for img in X:
        imlist.append(Image.fromarray(img))
    imlist[0].save(fname, save_all=True, append_images=imlist[1:])
    return

def get_points(fname, slices): #as list of integer tuples (slice, x, y)
    L = []
    with open(fname, 'r') as f:
        for line in f:
            L.append(tuple(map(int, line.split())))
    return(L)

def save_points(fname, lP):
    with open(fname, 'w') as f:
        for idx, slice in enumerate(lP):
            for pnt in slice:
                print(idx, pnt[0], pnt[1], file=f)
