import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re 
from increment import *
from check_bc import *
from e_sets import *
from steps import *
from def_mat import *
from step_sets import *
from merge_nodes import *
from recalc_surf import *
import itertools
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
		locs = np.array([X[element['n1']],
						X[element['n2']],
						X[element['n3']],
						X[element['n4']],
						X[element['n5']],
						X[element['n6']]])
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
	

"""
consolidates the x y z coloumns into a vector to make things easier
creates a vector from the template nodes to the centerline of the filament
args:
	nodes:		dataframe of nodes
	center:		
"""
def vects(nodes,center): 
	nodes['X'] = ""
	nodes['V'] = ""
	for i,node in nodes.iterrows():
		X = np.array([node['x'],node['y'],node['z']])
		nodes.at[i,'X'] = X
		nodes.at[i,'V'] = X-center 
	nodes.drop(['x','y','z'],axis = 1)
	return nodes


#loads the mesh cross section template 
template_nodes = pd.read_excel("cross_nodes.xlsx",index_col = 'index')
centerline = np.array([0.0002,0,0.0002])
template_nodes = vects(template_nodes,centerline)
template_elements = pd.read_excel("cross_elements.xlsx",index_col = 'index')
steps = pd.read_excel("steps.xlsx",index_col = "Step")
#starts the process
dr = 0
#start of the path
x0 = np.array([0,0,0.0002])
nodes = template_nodes[['type','ref','X','step','master']].copy()
nodes = nodes[0:0].copy()
elements = template_elements[0:0].copy()

#TOOL PATH
(x0,nodes, elements) = start_path(nodes,elements,template_nodes,template_elements,0,0,0.0004,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,1,0,0.0004,1,x0)
#(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,2,0.02,0.002,2,x0)

(x0,nodes,elements) = start_path(nodes,elements,template_nodes,template_elements,3,np.pi,0.0004,x0+np.array([0,0,0.0004]))
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,4,np.pi,0.0004,1,x0)
print(nodes['step'])
nodes,elements = merge_nodes(nodes,elements,5)
#plots the mesh
show_mesh(elements,nodes)
els = open("els.csv","w+")
nodes.to_csv(els)
#checks what nodes are at the build plate
nodes = dsp(nodes)

#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','ID','change']
changes = pd.DataFrame(columns = cols)

#LIST OF SURFACES
#index coloums of table of surfaces
indx = list(itertools.product([0],['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['REF']
surface_data = pd.DataFrame([0,1,2,3],index = idx,columns = surf_cols)
print (surface_data)





inp_file = open("analysis.inp","w+")
#MERGES THE NODES
merge_nodes(nodes,elements,3)
merge_nodes(nodes,elements,4)

#OUTPUTS EVERYTHING
gen_inp = lambda x: inp_file.write(x)
gen_inp(out_nodes(nodes))
gen_inp(out_elements(elements,nodes))
gen_inp(section())
gen_inp(materiel_model())

#EXTERNAL FREE SURFACES 

#buildplate surface
gen_inp(gensurf(elements,"BUILD_SURF",["DOWN"],step = [0,1]))
gen_inp(n_set(nodes,"BUILD_PLATE"))

#DEFINES STEPS
gen_inp(element_sets(elements,[0,1,3,4]))
#SURFACES FOR STEPS 
gen_inp(surf_step(elements,"UP",0))
gen_inp(surf_step(elements,"UP",1))

#STEPS
gen_inp(inital_step(elements,4,steps))
gen_inp(surf_cond(0,"UP","free_surface"))
gen_inp(surf_cond(1,"UP","free_surface"))
gen_inp(out_step(elements,1,steps))
gen_inp(out_step(elements,2,steps),deposition = False)
gen_inp(surf_cond(1,"UP","bond"))
gen_inp(out_step(elements,3,steps))
gen_inp(surf_cond(0,"UP","bond"))
gen_inp(out_step(elements,4,steps))




inp_file.close()
