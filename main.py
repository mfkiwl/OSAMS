import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re 
from increment import *
from check_bc import *
from e_sets import *
from steps import *

"""
show_mesh
plots the cross cection of the mesh template
args:
	elements: dataframe of elements
	nodes: dataframe of nodes
"""
def show_mesh(elements,nodes):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	X = nodes['X']
	for i,element in elements.iterrows():
		locs = np.array([X[element['n1']],
						X[element['n2']],
						X[element['n3']],
						X[element['n4']],
						X[element['n5']],
						X[element['n6']]])
		ax.scatter(locs[:,0],locs[:,1],locs[:,2])
	
	plt.show()
	

def vects(nodes,center): 
	nodes['X'] = ""
	nodes['V'] = ""
	for i,node in nodes.iterrows():
		X = np.array([node['x'],node['y'],node['z']])
		nodes.at[i,'X'] = X
		nodes.at[i,'V'] = X - center
	nodes.drop(['x','y','z'],axis = 1)
	return nodes


#loads the mesh cross section template 
template_nodes = pd.read_excel("G:\My Drive\PYthon\PROCESSMESH\cross_nodes.xlsx",index_col = 'index')
centerline = np.array([0,0.5,0])
template_nodes = vects(template_nodes,centerline)
print(template_nodes)
template_elements = pd.read_excel("G:\My Drive\PYthon\PROCESSMESH\cross_elements.xlsx",index_col = 'index')
steps = pd.read_excel("G:\My Drive\PYthon\PROCESSMESH\steps.xlsx",index_col = "Step")
#starts the process
dr = 0
#start of the path
x0 = np.array([0,0,0])
(x0,nodes, elements) = start_path(template_nodes,template_elements,0,dr,1,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,0,dr,2,2,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,1,0.01,2,2,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,2,0.02,2,2,x0)

#plots the mesh
show_mesh(elements,nodes)

#checks what nodes are at the build plate
nodes = dsp(nodes)



print(out_nodes(nodes))
print(out_elements(elements,nodes))
print(out_surf(nodes,"FREE_SURFACE"))
print(n_set(nodes,"BUILD_PLATE"))
print(element_sets(elements,[0,1,2]))
print(out_step(elements,0,steps))
