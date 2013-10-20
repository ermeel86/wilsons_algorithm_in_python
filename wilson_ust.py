#!/usr/bin/env python
"""
Wilson's algorithm for USTs on the 2d square lattice
(without periodic boundary conditions)
Eren Metin Elci <eren.metin.elci@gmail.com>
"""
import numpy as np
from sys import argv
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
# Lattice topology (square lattice)
def coords(k):
    return k - (k/L)*L,k/L
def idx(x,y):
    return x+y*L
def inc(a):
    return (a+1)%L
def dec(a):
    return (a-1+L)%L
def nbs(k):
    x,y = coords(k)
    nb = [0]
    if x > 0:
        nb[0]+=1
        nb.append(idx(dec(x),y))
    if x < L-1:
        nb[0]+=1
        nb.append(idx(inc(x),y))
    if y > 0:
        nb[0]+=1
        nb.append(idx(x,dec(y)))
    if y < L-1:
        nb[0]+=1
        nb.append(idx(x,inc(y)))
    return nb
# Construct adjacency list (first elements holds number of adjacent vertices)
adj_list = np.empty((nv,5),dtype=np.uint32)
for k in xrange(nv):
    n = nbs(k)
    adj_list[k,0] = n[0]
    adj_list[k,1:n[0]+1] = n[1:] 
# Array to keep track which vertices have already been visited (and in which iteration)
visited = -np.ones(nv,dtype=np.int32)
# List of edges part of the spanning tree
l = []
iteration = 0
# Start the iteration at vertex i and return 
# None if no edge is part of this loop erased path
# or return a list of all edges 
def le_path(i):
    global iteration
    v = i
    path = []
    while True:
        if visited[v] >= 0 and  visited[v] < iteration:
            break
        visited[v] = iteration
        n = adj_list[v][1+np.random.randint(adj_list[v][0])]
        if visited[n] < iteration:
            path.append((v,n))
        v = n
    return None if len(path) == 0 else path
# 0 iteration, construct T(0)
visited[0] = iteration 
for vi in xrange(1,nv):
    iteration+=1
    v = vi
    lp = le_path(v)
    if lp != None:
        l += lp
# Print dot format of spannig tree for square lattice base graph
# for usage with graphviz
def to_graphviz_square_lattice(l):
    global L,nv
    print "graph G { "
    lattice_const = .25
    indices = np.arange(nv,dtype=np.uint32)
    x_pos = indices/L
    y_pos = indices - x_pos*L
    for idx in indices:
        line_str = "\t{} [pos=\"{},{}!\", style=\"filled\",label=\"\" ,width=\"0.1\", height=\"0.1\",shape=\"point\"];\n".format(
        idx,lattice_const*x_pos[idx],lattice_const*y_pos[idx])
        print line_str
    for e in l:
        print e[0],"--",e[1],";"
    print "}"

to_graphviz_square_lattice(l)
