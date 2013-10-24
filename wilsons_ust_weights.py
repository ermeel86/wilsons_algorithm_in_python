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
        # to be able to select random edges prop. to their weight
        self.weights = weights.cumsum(axis=1)
        # checks if the network is stochastic
        # TODO: for future work try to do the graph modifications
        # indicated in david wilson's paper to still sample
        # from the random spanning tree ensemble
        assert np.alltrue(np.allclose(self.weights[:,-1],1))
        self.iteration=0
        # Array to keep track which vertices have already been visited
        # (and in which iteration)
        self.InTree = np.zeros(self.nv,dtype=np.uint8)
        self.Next = np.empty(self.nv,dtype=np.int32)
        self.tree_gen = False
        self.s_tree = None
    #############################################################################
    # get the index of the last occurence of element e in a
    def __rindex(self,a,e):
        for idx,v in enumerate(reversed(a)):
            if v==e:
                return len(a) - 1-idx
        raise ValueError
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
    def sample(self,seed=None):
        if seed != None:
            np.random.seed(int(seed))
        self.root = np.random.randint(self.nv)
        self.__RandomTreeWithRoot(self.root)
        self.__extract_tree_edges()
        return self.s_tree,self.root
    ############################################################################
    def __RandomTreeWithRoot(self,r):
        self.InTree[:] = 0
        self.InTree[r] = 1
        self.Next[r] = -1
        for i in xrange(self.nv):
            u = i
            while self.InTree[u] == 0:
                self.Next[u] = self.__random_edge(u)
                u = self.Next[u]
            u = i
            while self.InTree[u] == 0:
                self.InTree[u] = 1
                u = self.Next[u]
        self.tree_gen = True
    ############################################################################
    def __extract_tree_edges(self):
        assert self.tree_gen
        self.s_tree = []
        for i in xrange(self.nv):
            nb = self.Next[i]
            if nb >=0:
                self.s_tree.append((i,nb))
            else:
                self.root = i
###############################################################################




 
