import numpy as np
import pandas as pd
from .merge_group import *

"""
merges the psuedonodes aka step points
args:
	p_nodes:	dataframe of psuedonodes
	nodes:		model nodes
	elements:	model elements
	surfaces:	dataframe of surfaces (will change)
	BC_changes:	dataframe of heat transfer changes
returns:
	merged nodes and elements
	filled out changes in BC
	removes redundant surfaces
"""

def merge_p_nodes(p_nodes,nodes,elements,surfaces,BC_changes,tol = 0.00005):
	p_nodes.sort_values(by ='step', inplace = True)
	to_merge = p_nodes.copy()
	ls = p_nodes.index
	for i in ls: 
		c_node = p_nodes.iloc[i]
		x = c_node['x']
		y = c_node['y']
		z = c_node['z']
		stp = c_node['step']

		#revents redundant operations 

		to_merge = to_merge.drop(i)
		#finds node
		canidates = to_merge[to_merge['step'].values != int(stp)]
		if canidates.shape[0] == 0:
			continue
		canidates = canidates[np.isclose(canidates['x'].values[:,None],x,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue
	
		canidates = canidates[np.isclose(canidates['y'].values[:,None],y,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue

		canidates = canidates[np.isclose(canidates['z'].values[:,None],z,atol = tol).any(axis = 1)]
		if canidates.shape[0] == 0:
			continue

		#numpy getting confused
		s1 =  int(canidates['step'].values[0])
		s0 = int(stp)
		d1 = canidates['direction'].values[0]
		d0 = c_node['direction']
		#print(f"MERGED {s0}{d0} WITH {s1}{d1}")
		nodes,elements = merge_groups(nodes,s0,s1,d0,d1,elements)
		dropper = p_nodes.loc[(p_nodes['step'] == s1)&(p_nodes['direction'] == d1)].index
		ls = ls.drop(dropper)
		

		#activation step, surface creation step, and direction
		BC_change = [s1,s0,d0.upper(),'bond']

		#the redundant surface no longer exsits
		surfaces.loc[s1,d1.upper()] = 1 

		BC_changes.loc[len(BC_changes)] = BC_change
		
	return p_nodes,nodes,elements,surfaces,BC_changes



