import pandas as pd
import numpy as np

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

def start_path(nodes,elements,template_nodes,template_elements,step,dr,x0,x1):
	num_n = nodes.shape[0]
	num_ni = template_nodes.shape[0]
	num_e = elements.shape[0]
	
	#copies the face nodes 
	face_nodes0 = template_nodes[['type','ref','x','y','z','step','up','down','left','right']].copy()
	face_nodes1 = template_nodes[['type','ref','x','y','z','step','up','down','left','right']].copy()

	#nodes for the edges 17-20
	edge_template = template_nodes.loc[template_nodes['corner'] == 'YES']

	edge_nodes = edge_template[['type','ref','x','y','z','step','up','down','left','right']].copy()

	#number of edge nodes
	num_en = edge_nodes.shape[0]

	#centroid at end of step: 	x1
	#centroid at start of step:	x0	
	#rotates the face of the extrusion
	R = rotZ(dr)  

	#location along the extrude path of the mid edge nodes
	x12 = (x0 + x1)/2

	#translates the nodes
	face_nodes0[['x','y','z']] = template_nodes[['i','j','k']].dot(np.transpose(R)) + x0
	face_nodes1[['x','y','z']] = template_nodes[['i','j','k']].dot(np.transpose(R)) + x1

	#translates the edge nodes
	edge_nodes[['x','y','z']] = edge_template[['i','j','k']].dot(np.transpose(R)) + x12

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
