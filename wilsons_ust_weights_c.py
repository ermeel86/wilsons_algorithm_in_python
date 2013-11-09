#!/usr/bin/env python
"""
Wilson's algorithm for weighted STs. Works for archimedean lattices or 
graphs where every vertex has the same number of edges.

Core routines written in C
Eren Metin Elci <eren.metin.elci@gmail.com>
"""
from __future__ import  print_function
import ctypes
import numpy as np
PATH_PREFIX="/home/eren/Research/Simulations/Wilsons_Algorithm_UST/"
LIB_PATH="obj/lib_wilson.so"
wilson_c = ctypes.CDLL(PATH_PREFIX+LIB_PATH)




# specify paramter types
wilson_c.set_rng_seed.argtypes = [ctypes.c_int]
wilson_c.init_rng.argtypes = [ctypes.c_int]
wilson_c.RandomTreeWithRoot.argtypes = [ctypes.c_uint, ctypes.c_uint,ctypes.c_uint, ctypes.c_void_p,
        ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
wilson_c.set_rng_seed.restype = ctypes.c_ubyte
wilson_c.init_rng.restype = ctypes.c_ubyte
wilson_c.RandomTreeWithRoot.restype = ctypes.c_uint


class Wilsons_Algorithm(object):
    def __init__(self,adj_list,weights,seed=123456,d3=False):
        self.nv,self.coord = adj_list.shape
        self.adj_list = adj_list
        self.d3 = d3
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
        self.seed = seed
        self.init = wilson_c.init_rng(self.seed)
   ###############################################################################
    def __del__(self):
        if self.init:
            wilson_c.destroy_rng()
    ###############################################################################
    def sample(self,seed=None,p=1.):
        if seed != None:
            wilson_c.set_rng_seed(seed)
            self.seed = seed
        self.root = np.random.randint(self.nv)
        self.iteration = wilson_c.RandomTreeWithRoot(self.root,self.nv,
                self.coord, self.InTree.ctypes.data,self.adj_list.ctypes.data,
                self.Next.ctypes.data,self.weights.ctypes.data)

        self.tree_gen = True
        if p<1:
            self.__extract_tree_edges_prob(p)
        else:
            self.__extract_tree_edges()

        print("Sample with seed {} completed".format(self.seed))
        return self.s_tree,self.root
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
    ############################################################################
    def __extract_tree_edges_prob(self,p):
        assert self.tree_gen
        self.s_tree = []
        for i in xrange(self.nv):
            nb = self.Next[i]
            if nb >=0:
                if np.random.uniform() < p:
                    self.s_tree.append((i,nb))
            else:
                self.root = i
    ############################################################################
###############################################################################

