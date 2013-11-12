"""
Based on https://www.udacity.com/wiki/creating%20network%20graphs%20with%20python
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mayavi import mlab

import random

def draw_cubic_lattice(edges,l, graph_colormap='summer', bgcolor = (1, 1, 1),
                 node_size=0.03,
                 edge_color=(0.8, 0.8, 0.8), edge_size=0.02,
                 text_size=0.008, text_color=(0, 0, 0)):

    H=nx.Graph()

    # add edges
    H.add_nodes_from(np.arange(l**3))
    for e in edges:
        H.add_edge(e[0], e[1])
    
    G=nx.convert_node_labels_to_integers(H)
    # numpy array of x,y,z positions in sorted node order
    xyz = np.array([k for k in np.ndindex(l,l,l)])
    # scalar colors
    scalars=np.array(G.nodes())+5
    mlab.figure(1, bgcolor=bgcolor)
    mlab.clf()

    pts = mlab.points3d(xyz[:,2], xyz[:,1], xyz[:,0],
                        scalars,
                        scale_factor=node_size,
                        scale_mode='none',
                        colormap=graph_colormap,
                        resolution=20)

    #for i, (z, y, x) in enumerate(xyz):
    #    print i,x,y,z
    #    label = mlab.text(x, y, str(i), z=z,
    #                      width=text_size, name=str(i), color=text_color)
    #    label.property.shadow = True

    pts.mlab_source.dataset.lines = np.array(G.edges())
    tube = mlab.pipeline.tube(pts, tube_radius=edge_size)
    mlab.pipeline.surface(tube, color=edge_color)

    mlab.show() # interactive window
