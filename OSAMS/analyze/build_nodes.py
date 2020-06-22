import numpy as np
import pandas as pd


"""
this file contains functions to define the boundry conditions
"""
"""
checks if nodes are on the buildplate
"""
def build_nodes(nodes):
	f = lambda x: x[2] == 0
	nodes['type'].loc[nodes['X'].apply(f)] = 'BUILD_PLATE'
	return nodes
	
