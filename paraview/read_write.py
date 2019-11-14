import numpy as np
import struct
from evtk.hl import pointsToVTK
from evtk.hl import unstructuredGridToVTK
from evtk.vtk import VtkTriangle
from evtk.vtk import VtkTetra

###########################################################################
# functions
###########################################################################

def get_points(fname):            # (slice,x,y)
  L = []
  with open(fname, 'r') as f:
    for line in f:
      L.append(tuple(map(float, line.split())))
  L = np.array(L)
  L[:,[0, 1, 2]] = L[:,[1, 2, 0]] # permute to (x,y,z)
  return(L)

###########################################################################
def write_points(fname, verts, pdata=None):
  x = verts[:,0].copy() # deep copy required
  y = verts[:,1].copy()
  z = verts[:,2].copy()
  pointsToVTK(fname, x, y, z, data=pdata)  # write out vtu file
  return

###########################################################################
def write_tris(fname, verts, tris, data=None):
  x = verts[:,0].copy() # deep copy required
  y = verts[:,1].copy()
  z = verts[:,2].copy()
  ntris = tris.shape[0]
  conn = np.empty(3*ntris)
  for i in range(ntris):
    conn[3*i] = tris[i,0]-1 # index from zero
    conn[3*i+1] = tris[i,1]-1
    conn[3*i+2] = tris[i,2]-1
  offset = np.zeros(ntris, dtype=int)
  for i in range(ntris):
    offset[i] = 3*(i+1) 
  ctype = np.full(ntris, VtkTriangle.tid)
  unstructuredGridToVTK(fname, x, y, z, \
    connectivity=conn, offsets=offset, cell_types=ctype, \
    cellData=data, pointData=None)  # write out vtu file
  return

###########################################################################
def write_tets(fname, verts, tets, data=None):
  x = verts[:,0].copy() # deep copy required
  y = verts[:,1].copy()
  z = verts[:,2].copy()
  ntets = tets.shape[0]
  conn = np.empty(4*ntets)
  for i in range(ntets):
    conn[4*i] = tets[i,0]-1 # index from zero
    conn[4*i+1] = tets[i,1]-1
    conn[4*i+2] = tets[i,2]-1
    conn[4*i+3] = tets[i,3]-1
  offset = np.zeros(ntets, dtype=int)
  for i in range(ntets):
    offset[i] = 4*(i+1) 
  ctype = np.zeros(ntets)
  for i in range(ntets):
    ctype[i] = VtkTetra.tid 
  unstructuredGridToVTK(fname, x, y, z, \
    connectivity=conn, offsets=offset, cell_types=ctype, \
    cellData=data, pointData=None)  # write out vtu file
  return

###########################################################################
