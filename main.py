import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re 
from increment import *
from check_bc import *
from e_sets import *
from steps import *
from def_mat import *

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
	print(X)
	for i,element in elements.iterrows():
		locs = np.array([X[element['n1']-1],
						X[element['n2']-1],
						X[element['n3']-1],
						X[element['n4']-1],
						X[element['n5']-1],
						X[element['n6']-1]])
		ax.plot(locs[:,0]*1000,locs[:,1]*1000,locs[:,2]*1000)
	
	zz, yy = np.meshgrid(np.linspace(-1,1), np.linspace(0,2))
	xx = (yy * 0) 
	#ax.plot_surface(xx, yy, zz, alpha=0.2)
	ax.plot_surface(zz, yy, xx, alpha=0.2)
	ax.set_xlim3d(-1,1)
	ax.set_ylim3d(0,2)
	ax.set_zlim3d(-1,1)	
	ax.set_xlabel("x (mm)")
	ax.set_ylabel("y (mm)")
	ax.set_zlabel("z (mm)")
	ax.view_init(elev=90., azim=0)
	#ax.view_init(elev=0., azim=0)
	#ax.view_init(elev=0., azim=90)
	#ax.view_init(elev=45., azim=45)
	plt.show()
	

def vects(nodes,center): 
	nodes['X'] = ""
	nodes['V'] = ""
	for i,node in nodes.iterrows():
		X = np.array([node['x'],node['y'],node['z']])
		nodes.at[i,'X'] = X
		nodes.at[i,'V'] = center - X 
	nodes.drop(['x','y','z'],axis = 1)
	return nodes


#loads the mesh cross section template 
template_nodes = pd.read_excel("cross_nodes.xlsx",index_col = 'index')
centerline = np.array([0.0002,0,0.0002])
template_nodes = vects(template_nodes,centerline)
print(template_nodes)
template_elements = pd.read_excel("cross_elements.xlsx",index_col = 'index')
steps = pd.read_excel("steps.xlsx",index_col = "Step")
print(steps)
#starts the process
dr = 0
#start of the path
x0 = np.array([0,0,0.0002])
(x0,nodes, elements) = start_path(template_nodes,template_elements,0,dr,0.0004,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,1,dr,0.0004,1,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,2,0.25,0.0004,1,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,3,0.5,0.0004,1,x0)
#(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,2,0.02,0.002,2,x0)

#plots the mesh
show_mesh(elements,nodes)

#checks what nodes are at the build plate
nodes = dsp(nodes)

inp_file = open("analysis.inp","w+")

inp_file.write(out_nodes(nodes))
inp_file.write(out_elements(elements,nodes))
inp_file.write(section())
inp_file.write(materiel_model())
inp_file.write(out_surf(nodes,"FREE_SURFACE"))
inp_file.write(n_set(nodes,"BUILD_PLATE"))
inp_file.write(element_sets(elements,[0,1,2,3]))
inp_file.write(inital_step(elements,4,steps))
inp_file.write(out_step(elements,1,steps))
inp_file.write(out_step(elements,2,steps))
inp_file.write(out_step(elements,3,steps))

inp_file.close()
