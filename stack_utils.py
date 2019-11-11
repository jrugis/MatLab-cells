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
    for x in X:
        imlist.append(Image.fromarray(x))
    imlist[0].save(fname, save_all=True, append_images=imlist[1:])
    return

def save_points(fname, lP):
    with open(fname, 'w') as f:
        for ind,l in enumerate(lP):
            for p in l:
                print(ind,p[0],p[1], file=f)
