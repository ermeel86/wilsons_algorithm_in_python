#!/usr/bin/env python
"""
Wilson's algorithm for weighted STs on the 3d cubic lattice with p.b.c.
Allows to specify distinguished weights for horizontal,vertical and wrapping 
edges. The case of zero weight for wrapping edges corresponds to a lattice
without periodic boundary conditions.
Furthermore allows to do bond percolation on the generated spanning tree.

Eren Metin Elci <eren.metin.elci@gmail.com>
"""
from __future__ import print_function
import numpy as np
from sys import argv
###############################################################################
# Read possible command-line arguments
if len(argv) > 1:
    seed = int(argv[1])
else:
    seed = 123456
np.random.seed(seed)
if len(argv) > 2:
    L = int(argv[2])
else:
    L = 32
nv = L**3
nv_2d = L**2
C_Version = 1
if len(argv) > 3:
    C_Version = True if int(argv[3]) else 0
if C_Version:
    from wilsons_ust_weights_c import Wilsons_Algorithm
    print("***Using C routines")
else:
    from wilsons_ust_weights import Wilsons_Algorithm
if len(argv) > 4:
    p = float(argv[4])
else:
    p=1.
###############################################################################
# Lattice topology (here square lattice)
def coords(k):
    return k - (k/nv_2d)*nv_2d-((k-(k/nv_2d)*nv_2d)/L)*L,(k-(k/nv_2d)*nv_2d)/L,k/nv_2d
def idx(x,y,z):
    return x+y*L+z*nv_2d
def inc(a):
    return (a+1)%L
def dec(a):
    return (a-1+L)%L
# set to zero to prohibit wrapping edges; sets the weight of wrapping edges
wrapping_edge_weight = 0. 
# set weight for x edges
x_edge_weight = 1.
# set weight for y edges
y_edge_weight = 1.
# set weight for z edges
z_edge_weight = 1.

# horizontal and x,y,z edge weights have to be > 0 
assert x_edge_weight >0 and y_edge_weight >0 and z_edge_weight >0
##############################################################################
# generate adjacency list and weights
adj_list = np.empty((nv,6),dtype=np.uint64)
weights = np.empty_like(adj_list,dtype=np.float64)
for k in xrange(nv):
    x,y,z = coords(k)
    # east
    k_ = adj_list[k,0] = idx(dec(x),y,z)
    weights[k_,1] = weights[k,0] = (wrapping_edge_weight if x == 0 else 
    x_edge_weight)
    adj_list[k_,1] = k
    # north
    k_ = adj_list[k,2] = idx(x,dec(y),z)
    weights[k_,3]=weights[k,2] =( wrapping_edge_weight if y == 0 else 
    y_edge_weight)
    adj_list[k_,3] = k
    # down
    k_ = adj_list[k,4] = idx(x,y,dec(z))
    weights[k_,5]=weights[k,4] =( wrapping_edge_weight if z == 0 else 
    z_edge_weight)
    adj_list[k_,5] = k

###############################################################################
# sort adjacency lists according to weights
sort_indices = weights.argsort(axis=1)
for i in xrange(sort_indices.shape[0]):
    adj_list[i,:] = adj_list[i,sort_indices[i]]
# sort weights
weights.sort(axis=1) # inplace sort
# calculate transition prob. for random walk
weights /= weights.sum(axis=1)[:,np.newaxis]
###############################################################################
def wrapping_edge(e):
        x1,y1,z1 = coords(e[0])
        x2,y2,z2 = coords(e[1]) 
        return True if (abs(x2-x1) >1 or abs(y2-y1) > 1 or abs(z2-z1) > 1) else False
###############################################################################
def count_wrapping_edges(l):
    cnt = 0
    for e in l:
        if wrapping_edge(e):
            cnt+=1
    return cnt
###############################################################################
###############################################################################
if __name__ == "__main__":
    wa = Wilsons_Algorithm(adj_list,weights)
    s_tree,root = wa.sample(seed,p=p)
    print("Spanning Tree generated with total {} edges\
     and {} wrapping edges".format(len(s_tree),count_wrapping_edges(s_tree)))
