#!/usr/bin/env python
"""
Wilson's algorithm for weighted STs on the 2d square lattice with p.b.c.
Allows to specify distinguished weights for horizontal,vertical and wrapping 
edges. The case of zero weight for wrapping edges corresponds to a lattice
without periodic boundary conditions.

Eren Metin Elci <eren.metin.elci@gmail.com>
"""
from __future__ import print_function
from wilsons_ust_weights import Wilsons_Algorithm
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
nv = L**2
###############################################################################
# Lattice topology (here square lattice)
def coords(k):
    return k - (k/L)*L,k/L
def idx(x,y):
    return x+y*L
def inc(a):
    return (a+1)%L
def dec(a):
    return (a-1+L)%L
# set to zero to prohibit wrapping edges; sets the weight of wrapping edges
wrapping_edge_weight = 0. 
# set weight for vertical edges
vert_edge_weight = 1.
# set weight for horiz edges
horiz_edge_weight = 1.
# horizontal and vertical edge weights have to be > 0 
assert vert_edge_weight >0 and horiz_edge_weight >0
##############################################################################
# generate adjacency list and weights
adj_list = np.empty((nv,4),dtype=np.uint32)
weights = np.empty_like(adj_list,dtype=np.float64)
for k in xrange(nv):
    x,y = coords(k)
    # left
    k_ = adj_list[k,0] = idx(dec(x),y)
    weights[k_,1] = weights[k,0] = (wrapping_edge_weight if x == 0 else 
    horiz_edge_weight)
    adj_list[k_,1] = k
    # up
    k_ = adj_list[k,2] = idx(x,dec(y))
    weights[k_,3]=weights[k,2] =( wrapping_edge_weight if y == 0 else 
    vert_edge_weight)
    adj_list[k_,3] = k
###############################################################################
# sort adjacency lists according to weights
sort_indices = weights.argsort(axis=1)
for i in xrange(sort_indices.shape[0]):
    adj_list[i,:] = adj_list[i,sort_indices[i]]
# sort weights
weights.sort(axis=1) # inplace sort
# calculate transition prob. for random walk
weights /= weights.sum(axis=1)[:,np.newaxis]
weights = weights.cumsum(axis=1)
###############################################################################
###############################################################################
def wrapping_edge(e):
        x1,y1 = coords(e[0])
        x2,y2 = coords(e[1]) 
        return True if (abs(x2-x1) >1 or abs(y2-y1) > 1) else False
###############################################################################
#Print dot format of spannig tree for square lattice base graph
# for usage with graphviz
def to_graphviz_square_lattice(l,L,seed):
    nv = L**2 
    fname = "./stree_l{}_s{}.dot".format(L,seed)
    try:
        f = open(fname,"w")
        print("graph G { ",file=f)
        lattice_const = .25
        indices = np.arange(nv,dtype=np.uint32)
        x_pos = indices/L
        y_pos = indices - x_pos*L
        for idx in indices:
            line_str = "\t{} [pos=\"{},{}!\", style=\"invisible\",label=\"\""
            line_str+=",width=\"0.001\", height=\"0.001\"];\n"
            line_str = line_str.format(
            idx,lattice_const*y_pos[idx],lattice_const*x_pos[idx])
            print(line_str,file=f)
        for e in l:
            if not wrapping_edge(e):
                print(e[0],"--",e[1],";",file=f)
            else:
                print("//",e[0],"--",e[1],";",file=f)
        print("labelloc=\"t\";",file=f)
        lbl = "Spanning tree on {}x{} square lattice (seed = {})"
        lbl = lbl.format(L,L,seed)
        print("label=\"{}\";".format(lbl),file=f)
        print("}",file=f)
        f.close()
    except Exception as e:
        print("Could not write to file {}".format(fname))
        print("Exception string: {}".format(str(e)))
    else:
        print("Graphviz '{}' file successfully created!".format(fname))
###############################################################################
def count_wrapping_edges(l):
    cnt = 0
    for e in l:
        if wrapping_edge(e):
            cnt+=1
    return cnt
###############################################################################
wa = Wilsons_Algorithm(L,adj_list,weights)
s_tree = wa.sample()
print("Spanning Tree generated with total {} edges\
 and {} wrapping edges".format(len(s_tree),count_wrapping_edges(s_tree)))
to_graphviz_square_lattice(s_tree,L,seed)
