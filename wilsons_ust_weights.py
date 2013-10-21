#!/usr/bin/env python
"""
Wilson's algorithm for weighted STs. Works for archimedean lattices or 
graphs where every vertex has the same number of edges.

Eren Metin Elci <eren.metin.elci@gmail.com>
"""
from __future__ import print_function
import numpy as np
from sys import argv
from itertools import chain

class Wilsons_Algorithm(object):
    def __init__(self,l,adj_list,weights):
        self.L = l
        self.nv = l**2
        self.adj_list = adj_list
        self.weights = weights
        self.iteration=0
        # Array to keep track which vertices have already been visited
        # (and in which iteration)
        self.visited = -np.ones(self.nv,dtype=np.int32)
    #############################################################################
    # get the index of the last occurence of element e in a
    def __rindex(self,a,e):
        for idx,v in enumerate(reversed(a)):
            if v==e:
                return len(a) - 1-idx
        raise ValueError
    ############################################################################
    # visit all vertices in l with value i
    def __visit_vertices(self,l,i):
        for v in l:
            self.visited[l] = i
    ############################################################################
    # Choose an edge from v's adjacency list (randomly)
    def __random_edge(self,v,uniform_weights=False):
        if uniform_weights:
            return self.adj_list[v][np.random.randint(4)]
        else:
            r = np.random.uniform()
            for i in xrange(4):
                if self.weights[v,i] > r:
                    return self.adj_list[v,i]

   ###############################################################################
    # return loop-erasure of a simple random walk
    # loops are erased in chronological order
    def __srw_to_lerw(self,srw_p):
        # l needs to be a tuple/list of vertices, actually
        # the path corresponding to the random walk
        n = len(srw_p)
        if n == 0:
            return None
        gk = srw_p[0]
        lerw_p = []
        while True:
            lerw_p.append(gk)
            sk = self.__rindex(srw_p,gk)
            if sk == n-1:
                return lerw_p
            else:
                gk = srw_p[sk+1]
        return lerw_p
    ############################################################################
    # Start a simple random walk (srw) at vertex i
    # until reaching a vertex in the tree of iteration <i, i.e.
    # a vertex with visited value >= 0 and <i.
    # Return the path as a list 
    def __srw_starting_at(self,i):
        v = i
        path = [v]
        while True:
            if self.visited[v] >= 0 and  self.visited[v] < self.iteration:
                return path
            n = self.__random_edge(v) 
            path.append(n)
            v = n
    ############################################################################
    # get a list of edges based on the path
    def __path_to_edges(self,path):
        e = []
        for i in xrange(1,len(path)):
            e.append((path[i-1],path[i]))
        return e
    ############################################################################
    def sample(self,seed=None):
        if seed != None:
            np.random.seed(int(seed))
        self.s_tree = None
        self.visited[0] = self.iteration 
        # Iterate over all vertices
        for vi in xrange(1,self.nv):
            self.iteration+=1
            srw_p = self.__srw_starting_at(vi)
            lerw_p = self.__srw_to_lerw(srw_p)
            self.__visit_vertices(lerw_p,self.iteration)
            # Explain this
            if len(lerw_p) > 1:
                if self.s_tree == None:
                    self.s_tree = self.__path_to_edges(lerw_p)
                else:
                    self.s_tree = chain(self.s_tree, self.__path_to_edges(lerw_p))
        # reset
        self.visited[:] = -1
        return [e for e in self.s_tree]
###############################################################################
 
