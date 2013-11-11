#!/usr/bin/env python
from __future__ import  print_function
import ctypes
import numpy as np
PATH_PREFIX="/home/eren/Research/Simulations/Wilsons_Algorithm_UST/"
LIB_PATH="obj/lib_cluster_statistics.so"
clust_stat = ctypes.CDLL(PATH_PREFIX+LIB_PATH)




# specify paramter types
clust_stat.cluster_stat_init_cubic.argtypes = [ctypes.c_ulonglong]
clust_stat.cluster_stat_analyse_cubic.argtypes=[ctypes.c_void_p,ctypes.c_ulonglong]

clust_stat.cluster_stat_init_cubic.restype = ctypes.c_ubyte
clust_stat.cluster_stat_analyse_cubic.restype = ctypes.c_ulonglong
clust_stat.cluster_stat_size_giant.restype = ctypes.c_ulonglong
clust_stat.cluster_stat_num_cluster.restype = ctypes.c_ulonglong
clust_stat.cluster_stat_log_csm2.restype = ctypes.c_double
clust_stat.cluster_stat_log_csm4.restype = ctypes.c_double


class Cluster_Statistics_Cubic(object):
    def __init__(self,l):
        self.length_1d = np.uint64(l)
        self.init = True if clust_stat.cluster_stat_init_cubic(self.length_1d) else False
    def cluster_analyse(self,edge_list):
        return clust_stat.cluster_stat_analyse_cubic(edge_list.ctypes.data,np.uint64(len(edge_list)/2))
    def observables(self):
        return (clust_stat.cluster_stat_num_cluster(),clust_stat.cluster_stat_size_giant(), 
                clust_stat.cluster_stat_log_csm2(), clust_stat.cluster_stat_log_csm4())
    def __del__(self):
        clust_stat.cluster_stat_destroy()
