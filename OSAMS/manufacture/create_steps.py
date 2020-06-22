import numpy as np
import pandas as pd 
from .partition_step import *
layer_z = 0.3
def angle_between(v1, v2):
	theta = (np.arctan2(np.cross(v1,v2),np.dot(v1,v2))[2])%(2*np.pi)
	return theta
"""
create_steps: creates the extrusion step definitions and creates the mesh for the analysis
args:
	partitions:		list of distances along the toolpath where two different steps meet
	path_funct:		machine state as a function of distance along toolpath
returns:
	steps:			list of steps
"""
def create_steps(partitions,path_funct,nodes,elements,template):
	
	#initializes step dataframe
	steps = pd.DataFrame(columns = ['BP_T','dt','fan','type','layer','extruder'])
	jump = True
	step = 0
	face = 0
	d1 = partitions.iloc[0]
	for i in range(1,len(partitions)):
		
		#generates the step from the tool path data
		d2 = partitions.iloc[i]
		mid = (d1+d2)/2
		row = {'BP_T':0 , 'dt': 0 ,'type': 0, 'layer': 0, 'extruder' :0, 'fan': 0}
		row['dt'] = path_funct['time'](d2) - path_funct['time'](d1)
		row['BP_T'] = path_funct['b_temp'](d1)
		row['layer'] =(path_funct['z'](d1)/layer_z)
		row['type'] = (path_funct['extruding'](d2))
		row['extruder'] = path_funct['temp'](d1)
		row['SOL_T'] = 'SEPARATED'
		row['fan'] = path_funct['fan'](d1)
		if (row['type'] == 1):
			face,nodes,elements = partition_step(d2,d1,path_funct,jump,step,nodes,elements,template,face)
			jump = False
		else:
			jump = True

		steps = steps.append(row,ignore_index = True)
		d1 = d2

		#increments the step
		step += 1
	
	return steps,nodes,elements
