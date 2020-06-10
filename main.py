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
from analysis_step import *
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

#Simulated Machine


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
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,0,0,0.0004,1,x0)

x0 = np.array([0.0004,0,0.0002])
(x0,nodes, elements) = start_path(nodes,elements,template_nodes,template_elements,1,0,0.0004,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,1,0,0.0004,1,x0)

#(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,2,0.02,0.002,2,x0)

x0 = np.array([0.0,0,0.0006])
(x0,nodes, elements) = start_path(nodes,elements,template_nodes,template_elements,3,0,0.0004,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,3,0,0.0004,1,x0)

x0 = np.array([0.0004,0,0.0006])
(x0,nodes, elements) = start_path(nodes,elements,template_nodes,template_elements,4,0,0.0004,x0)
(x0,nodes, elements) = increment(nodes,elements,template_nodes,template_elements,4,0,0.0004,1,x0)

#plots the mesh
#checks what nodes are at the build plate
nodes = dsp(nodes)

#DEPOSITION STEP PLACEHOLDER 
place = [0,1,3,4]

#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','d_step','side','change']
BC_changes = pd.DataFrame(columns = cols)

#LIST OF SURFACES
#index coloums of table of surfaces
#CREATE THING TO MAKE SURFACE DF

indx = list(itertools.product(place,['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['ref']
surfaces = pd.DataFrame(index = idx,columns = surf_cols)
surfaces['ref'] = -1


#merges and recalculates BCs for all deposition steps
for i in place:
	(nodes,elements, surfaces, BC_changes) = analysis_step(nodes,elements,surfaces,BC_changes,i)

#drops duplicate boundry conditions
BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))

inp_file = open('analysis.inp','w+')

gen_inp = lambda x: inp_file.write(x)
nodes = dsp(nodes)

gen_inp(out_nodes(nodes))
gen_inp(out_elements(elements,nodes))
gen_inp(materiel_model())
gen_inp(section())
gen_inp(build_surf(elements,steps))
gen_inp(element_sets(elements,steps))
gen_inp(n_set(nodes,"BUILD_PLATE"))
gen_inp(gen_surf(elements,surfaces))

gen_inp(inital_step(elements,5,steps,surfaces))
gen_inp(out_step(elements,1,steps,BC_changes))
gen_inp(out_step(elements,2,steps,BC_changes,deposition = False))
gen_inp(out_step(elements,3,steps,BC_changes))
gen_inp(out_step(elements,4,steps,BC_changes))

#MERGES THE NODES
inp_file.close()
