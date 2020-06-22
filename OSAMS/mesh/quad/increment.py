import pandas as pd
import numpy as np
from increment import *
"""
this file is responsible for creating nodes, and renumbering elements nodes and extruding the mesh on an element level
""" 

x_hat = np.array([1,0,0])
def average_angle(theta1,theta2):
	U1 =  np.array([np.cos(theta1), np.sin(theta1),0])
	U2 =  np.array([np.cos(theta2), np.sin(theta2),0])
	U = (U1+ U2)/2
	return angle_between(x_hat,U)

def angle_between(v1, v2):
	theta = (np.arctan2(np.cross(v1,v2),np.dot(v1,v2))[2])
	return theta
"""
extrudes the template cross section by a single element in a path
args:
	nodes:				dataframe of current nodes
	elements:			dataframe of current elements
	tempplate_nodes: 	dataframe of nodes of the template
	element_nodes:		dataframe of elements of the current template
	step:				step this increment belongs to
	d0:					extrusion angle at start 
	dr:					extrusion angle	at end
	dist:				element depth
	x0:					location of the nozzle at the start of the path
returns:
	nodes:				dataframe of nodes
	elements:			dataframe of elements
"""

def mesh_extrude(nodes,elements,template_nodes,template_elements,step,d0,dr,x0,x12,x1):
	num_n = nodes.shape[0]
	num_ni = template_nodes.shape[0]
	num_e = elements.shape[0]
	
	#copies the face nodes 
	face_nodes = template_nodes[['type','ref','X','step','master']].copy()

	#nodes for the edges 17-20
	edge_template = template_nodes.loc[template_nodes['corner'] == 'YES']

	edge_nodes = edge_template[['type','ref','X','step','master']].copy()

	#number of edge nodes
	num_en = edge_nodes.shape[0]

	#centroid at end of step: 	x1
	#centroid at start of step:	x0	
	#rotates the face of the extrusion
	R = rotZ(dr)

	R2 = rotZ(average_angle(dr,d0))

	#location along the extrude path of the mid edge nodes
	#translates the nodes
	face_nodes['X'] = template_nodes['V'].apply(lambda x: x1 + np.matmul(R,np.transpose(x)))
	#print(template_nodes[['x','y','z']].dot(np.transpose(R)))
	#print(face_nodes['X'])

	#translates the edge nodes
	edge_nodes['X'] = edge_template['V'].apply(lambda x: x12 + np.matmul(R2,np.transpose(x)))

	current_elements = template_elements.copy()
	# M  = 8 for 20 node
	#nodes of exisiting face 
	f4 = lambda x: x+num_n-(num_ni+num_en)
	current_elements['n1'] = 	current_elements['n1'] .apply(f4)
	current_elements['n2'] = 	current_elements['n2'] .apply(f4)
	current_elements['n3'] = 	current_elements['n3'] .apply(f4)
	current_elements['n4'] = 	current_elements['n4'] .apply(f4)
	current_elements['n9'] = 	current_elements['n9'] .apply(f4)
	current_elements['n10'] = 	current_elements['n10'].apply(f4)
	current_elements['n11'] = 	current_elements['n11'].apply(f4)
	current_elements['n12'] = 	current_elements['n12'].apply(f4)

	#new face
	f4 = lambda x: x+num_n
	new_nodes = ['n5','n6','n7','n8','n13','n14','n15','n16']
	current_elements[new_nodes] = current_elements[new_nodes].apply(f4)

	#mid edge nodes 
	f4 = lambda x: x+num_n+(num_ni)
	new_nodes = ['n17','n18','n19','n20']
	current_elements[new_nodes] = current_elements[new_nodes].apply(f4)

	#sets process step
	current_elements['step'] = step
	current_nodes=pd.concat([face_nodes,edge_nodes], ignore_index = True)
	current_nodes['step'] = step

	#changes the node indexes of the mesh_increment
	nodes.append(current_nodes)
	elements = pd.concat([elements,current_elements],ignore_index = True)
	nodes = pd.concat([nodes,current_nodes],ignore_index = True)
	return  nodes, elements

"""
creates a new filament
"""
def start_path(nodes,elements,template_nodes,template_elements,step,dr,x0,x1):
	num_n = nodes.shape[0]
	num_ni = template_nodes.shape[0]
	num_e = elements.shape[0]
	
	#copies the face nodes 
	face_nodes0 = template_nodes[['type','ref','X','step','master']].copy()
	face_nodes1 = template_nodes[['type','ref','X','step','master']].copy()

	#nodes for the edges 17-20
	edge_template = template_nodes.loc[template_nodes['corner'] == 'YES']

	edge_nodes = edge_template[['type','ref','X','step','master']].copy()

	#number of edge nodes
	num_en = edge_nodes.shape[0]

	#centroid at end of step: 	x1
	#centroid at start of step:	x0	
	#rotates the face of the extrusion
	R = rotZ(dr)  

	#location along the extrude path of the mid edge nodes
	x12 = (x0 + x1)/2

	#translates the nodes
	face_nodes0['X'] = template_nodes['V'].apply(lambda x: x0 + np.matmul(R,np.transpose(x)))
	face_nodes1['X'] = template_nodes['V'].apply(lambda x: x1 + np.matmul(R,np.transpose(x)))

	#translates the edge nodes
	edge_nodes['X'] = edge_template['V'].apply(lambda x: x12 + np.matmul(R,np.transpose(x)))

	current_elements = template_elements.copy()
	# M  = 8 for 20 node
	#nodes of exisiting face 
	f4 = lambda x: x+num_n
	current_elements['n1'] = 	current_elements['n1'] .apply(f4)
	current_elements['n2'] = 	current_elements['n2'] .apply(f4)
	current_elements['n3'] = 	current_elements['n3'] .apply(f4)
	current_elements['n4'] = 	current_elements['n4'] .apply(f4)
	current_elements['n9'] = 	current_elements['n9'] .apply(f4)
	current_elements['n10'] = 	current_elements['n10'].apply(f4)
	current_elements['n11'] = 	current_elements['n11'].apply(f4)
	current_elements['n12'] = 	current_elements['n12'].apply(f4)

	#new face
	f4 = lambda x: x+num_n+num_ni
	new_nodes = ['n5','n6','n7','n8','n13','n14','n15','n16']
	current_elements[new_nodes] = current_elements[new_nodes].apply(f4)

	#mid edge nodes 
	f4 = lambda x: x+num_n+(num_ni+num_ni)
	new_nodes = ['n17','n18','n19','n20']
	current_elements[new_nodes] = current_elements[new_nodes].apply(f4)

	current_nodes = pd.concat([face_nodes0,face_nodes1,edge_nodes],ignore_index = True)
	current_nodes['step'] = step
	current_elements['step'] = step
	
	nodes = pd.concat([nodes,current_nodes],ignore_index = True)
	elements = pd.concat([elements,current_elements],ignore_index = True)

	return nodes, elements

"""
rotates about the GLOBAL z axis
args:
	theta:		angle
returns:
	rotation matrix
"""
def rotZ(theta):
	R = np.array([[np.cos(theta),	-np.sin(theta), 0],
				  [np.sin(theta),	np.cos(theta), 0],
				  [0,0,1]])
	return R

"""
increment:
DEPRECATED 
steps the mesh by one process step
one process step is one .INP file
args:
	nodes:				dataframe of current nodes
	elements:			dataframe of current elements
	tempplate_nodes: 	dataframe of nodes of the template
	element_nodes:		dataframe of elements of the current template
	step:				step this increment belongs to
	dr:					direction
	dist:				distance of extrusion 
	m_inc:				number of mesh increments
	x0:					centroid of current filament
returns:
	nothing
"""
def increment(nodes,elements,template_nodes,template_elements,step,dr,dist,m_inc,x0):
	inc_dist = dist/m_inc
	n_nodes = int(template_nodes.shape[0] + 16)
	for i in range(0,m_inc):
		(x0,nodes,elements) = mesh_extrude(nodes,elements,template_nodes,template_elements,step,dr,inc_dist,x0) 
	
	#makes nodes at the end of the extrusion step not master nodes
	nodes.iloc[-n_nodes:-1]['master'] = 'NO'
	return x0,nodes,elements



