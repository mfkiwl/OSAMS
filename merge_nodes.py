import pandas as pd
import numpy as np
def replace(x,rp,rw):
	if (x == rp):
		x = rw
	return x
"""
merge_nodes
merges nodes with the same coordinates and handles changing of BCs
args:
	nodes:		dataframe of the nodes
	step:		the nodes of the step that needs to be merged
	tolerance:	acceptable merge tolerance
returns:
	nodes that were merged w/ one another
"""
def merge_nodes(nodes,elements,step,surfaces,BC_changes,tol = 0.0001):
	step_nodes = nodes.loc[lambda nodes: nodes['step'] == step]
	lower_nodes = nodes.loc[nodes['step'] < step] 
	print(step_nodes.index)

	#goes through the nodes that have yet to be merged
	for i,node in step_nodes.iterrows():
		
		#merge criteria
		close = lambda x: np.linalg.norm(x-node['X']) < tol 
	
		#creates a list of nodes matching merge criteria
		#if merge criteria correct then only one node should be in this
		canidates = lower_nodes.loc[nodes['X'].apply(close)]
		canidates = canidates.loc[canidates.index != i]

		#can this node be merged?
		if (canidates.shape[0] >= 1):
			#if any nodes match the merge criteria, merge the first one
			nodes = nodes.drop(i)

			#is there a slave surface associated with this node?
			if (node['master'] != 'NO'):
				m_node = canidates.iloc[0]

				#deposition step and slave surface of the merged node
				BC_change = [step,m_node['step'],m_node['master'],'bond']

				#flags surface as redundant
				surfaces.at[(step,node['master']),'ref'] = 1 

				#appends change to BC changes
				BC_changes.loc[len(BC_changes)] = BC_change

			#remove all instances of the rundundant node
			elements[['n1','n2' ,'n3','n4','n5','n6']] = elements[['n1','n2' ,'n3','n4','n5','n6']].replace(i,canidates.index[0])
			#print(f"MERGED {i} AND {canidates.index[0]}")

	return nodes,elements,surfaces,BC_changes
