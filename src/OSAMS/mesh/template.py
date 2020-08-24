import pandas as pd
import numpy as np
"""
this file is responsible for fetching and preprocessing the template mesh
"""


class template:
	"""
	consolidates the x y z coloumns into a vector to make things easier
	creates a vector from the template nodes to the centerline of the filament
	args:
		nodes:		dataframe of nodes
		center:		
	"""
	def __init__(self,f_w,f_h,template='1BRICK.xlsx'):
		self.filament_width = f_w
		self.filament_height = f_h 
		self.nodes = pd.read_excel(template,sheet_name = 'NODES', index_col = 'index')
		self.elements = pd.read_excel(template,sheet_name = 'ELEMENTS', index_col = 'index')
		self.e_type = pd.read_excel(template, sheet_name = 'ETYPE', index_col = 'analysis')
		self.nodes = self.vects(self.nodes) 

	def vects(self,nodes): 
		#nodes['X'] = ""
		#nodes['V'] = ""
		centerline = np.array([self.filament_width,0,0])/2		#centerline: the xy coordinate of the centerline of the mesh
		nodes[['z']] = nodes[['z']] * self.filament_height
		nodes[['x']] = nodes[['x']] * self.filament_width
		nodes[['i','j','k']] = nodes[['x','y','z']] - centerline
		nodes.drop(['x','y','z'],axis = 1)
		return nodes

