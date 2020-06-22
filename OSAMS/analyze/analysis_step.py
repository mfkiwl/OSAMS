import pandas as pd
import numpy as np
from .merge_nodes import *
"""
generates everything short of the INP lines
args:
	nodes:	the nodes of the 
"""
def analysis_step(nodes,elements,surfaces,BC_changes,step):

	#merges the nodes and recalculates the surfaces
	(nodes,elements,surfaces,BC_changes) = merge_nodes(nodes,elements,step,surfaces,BC_changes)

	return (nodes,elements,surfaces,BC_changes)

	

	
