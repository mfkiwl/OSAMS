import pandas as pd
import numpy as np
def replace(x,rp,rw):
	if (x == rp):
		x = rw
	return x
"""
merge_nodes
merges nodes with the same coordinates
args:
	nodes:		dataframe of the nodes
	step:		the nodes of the step that needs to be merged
	tolerance:	acceptable merge tolerance
returns:
	nodes that were merged w/ one another
"""
def merge_nodes(nodes,elements,step,tol = 0.00001):
	step_nodes = nodes.loc[lambda nodes: nodes['step'] == step]
	print(step_nodes.index)

	#goes through the nodes that have yet to be merged
	for i,node in step_nodes.iterrows():
		
		#merge criteria
		close = lambda x: np.linalg.norm(x-node['X']) < tol 
	
		#creates a list of nodes matching merge criteria
		#if merge criteria correct then only one node should be in this
		canidates = nodes.loc[nodes['X'].apply(close)]
		canidates = canidates.loc[canidates.index != i]
		#determines if nodes are close to the node to merge
		if (canidates.shape[0]):
			#if any nodes match the merge criteria, merge the first one
			nodes = nodes.drop(i)
			if (nodes['master'] != 'NO'):
				"NOPE"
				#GET SURFACE AT STEP N AND ORIENTATION
				

				#BC_changes.append({'ID': ID}, {'change': 'bond'}, {'step': step}, ignore_index = True)

			elements[['n1','n2' ,'n3','n4','n5','n6']] = elements[['n1','n2' ,'n3','n4','n5','n6']].replace(i,canidates.index[0])
			print(f"MERGED {i} AND {canidates.index[0]}")

	return nodes,elements
