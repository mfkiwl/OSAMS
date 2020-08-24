'''
MERGE GROUPS
Theory: Merges the nodes on a given surface and drops the higher numbered node
Changes:
Date		Author		Changes
8/19/20 	Chris Bock	NONE
'''
import pandas as pd
import numpy as np

e_list = [f"n{i}" for i in range(1,21)]
"""
merges node from step s0 on side d0 to step s1 side d1
args:
	nodes:	model nodes
	s0:		the lower step
	s1:		the higher step
	d0:		direction for s0
	d1:		direction for s1
	elements:	model elements
	tol:	tolerance for merging (m)
returns:
	merged nodes and elements
"""
def merge_groups(nodes,s0,s1,d0,d1,elements, tol = 0.00001):

	#gets the nodes of the two surfaces to merge
	lower = nodes.loc[(nodes['step'].isin([s0-1,s0,s0+1])) & (nodes[d0])].copy()

	upper = nodes.loc[(nodes['step'].isin([s1+1,s1,s1-1])) & (nodes[d1])].copy()

	close = lambda x,y: np.linalg.norm(x-y) < tol 
	for i,node in lower.iterrows():

		#finds close nodes
		x = node['x']
		y = node['y']
		z = node['z']

		canidates = upper[np.isclose(upper['x'].values[:,None],x,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue
	
		canidates = canidates[np.isclose(canidates['y'].values[:,None],y,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue

		canidates = canidates[np.isclose(canidates['z'].values[:,None],z,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue

		if (canidates.shape[0] > 0):
			merged = canidates.index[0]
			ind = node['ref']
			#ex = canidates.at[merged,'X']
			step = canidates['step'].iloc[0]
			upper.drop(merged,inplace = True)
			#nodes.at[i,'X'] = (w+ex)/2


			nodes.at[merged,'ref'] = ind
			#step_els = elements.loc[elements['step'] == step]

			elements[e_list] = elements[e_list].replace(merged,ind)
	return nodes,elements
			
