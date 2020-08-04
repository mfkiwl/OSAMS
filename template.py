import pandas as pd
import numpy as np
"""
this file is responsible for fetching and preprocessing the template mesh
"""

#filament_width = 0.01
#filament_height = 0.004064
filament_width = 0.000914
filament_height = 0.000254
centerline = np.array([filament_width,0,0])/2		#centerline: the xy coordinate of the centerline of the mesh (NORMALLY ZERO) also dictates the rotation of the mesh
"""
consolidates the x y z coloumns into a vector to make things easier
creates a vector from the template nodes to the centerline of the filament
args:
	nodes:		dataframe of nodes
	center:		
"""
def vects(nodes,center): 
	#nodes['X'] = ""
	#nodes['V'] = ""
	nodes[['z']] = nodes[['z']] * filament_height
	nodes[['x']] = nodes[['x']] * filament_width
	nodes[['i','j','k']] = nodes[['x','y','z']] - centerline

	"""
	for i,node in nodes.iterrows():
		X = np.array([node['x'],node['y'],node['z']])
		nodes.at[i,['i','j','z']] = X-centerline
	"""

	nodes.drop(['x','y','z'],axis = 1)
	print(nodes)
	return nodes

nodes = pd.read_excel("1BRICK.xlsx",sheet_name = 'NODES', index_col = 'index')
print(nodes.head())
elements = pd.read_excel("1BRICK.xlsx",sheet_name = 'ELEMENTS', index_col = 'index')
e_type = pd.read_excel("1BRICK.xlsx", sheet_name = 'ETYPE', index_col = 'analysis')
nodes = vects(nodes,centerline)
