
import numpy as np
import read_write as rw

###################################
###################################
IMAGE_SIZE_XY = 1024.0
IMAGE_SIZE_Z = 26.0 
ACTUAL_XY = 80.0
ACTUAL_STEP_Z = 2.0
ACTUAL_GLYPH = 3.0

###################
SCALE_X = ACTUAL_XY / IMAGE_SIZE_XY 
SCALE_Y = SCALE_X
SCALE_Z = ACTUAL_STEP_Z

###########################################################################
# main program
###########################################################################

fname = 'points'

verts = rw.get_points(fname+'.txt')
print(verts)

verts[:,0] *= SCALE_X
verts[:,1] *= SCALE_Y
verts[:,2] *= SCALE_Z
print(verts)

rw.write_points(fname, verts)

#rw.write_tris("basal_"+fname, lverts[i], ltris[i][btrisi-1]) # has all the verts
#rw.write_tets("elements_"+fname, lverts[i], ltets[i], data={"dfa" : ldfa_tet[i], "dfb" : dfb})
