'''
CREATE STEP
creates the inital mesh, with all of the associated data 
THEORY
The tool path is split into steps based on a maximum time step, then these steps are split into elements
CHANGES
DATE		AUTHOR		CHANGE
2020.08.24	Chris Bock	Fixed bug with setting the layer
2020.8.19	Chris Bock	None
'''
import pandas as pd
import math
from .partition_step import *
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
def create_steps(partitions,path_funct,nodes,elements,template,el_step = 1):
	
	#initializes step dataframe
	steps = pd.DataFrame(columns = ['BP_T','dt','fan','type','layer','extruder'])
	jump = False 
	red = True 
	step = 0
	face = 0
	d1 = partitions.iloc[0]
	el_size = template['elements'].shape[0]
	face_surfs = pd.DataFrame(columns=['step','elements','face','pos'])
	#nodes to make merging faster 
	psuedo_nodes = pd.DataFrame(columns = ['step','direction', 'x' ,'y','z'])
	z0 = None
	for i in range(1,len(partitions)):
		
		#generates the step from the tool path data
		d2 = partitions.iloc[i]
		mid = (d1+d2)/2
		row = {'BP_T':0 , 'dt': 0 ,'type': 0, 'layer': 0, 'extruder' :0, 'fan': 0}
		row['dt'] = path_funct['time'](d2) - path_funct['time'](d1)
		row['BP_T'] = path_funct['b_temp'](d2)
		row['layer'] = -1
		row['type'] = (path_funct['extruding'](d2))
		row['extruder'] = path_funct['temp'](d2)
		row['SOL_T'] = 'SEPARATED'
		row['fan'] = path_funct['fan'](d2)
		if(z0 != None):
			row['layer'] = math.floor((((path_funct['z'](d2)/1000)-z0+0.000001)/template['height']))
			
		

		#psuedo nodes
		if (row['type'] == 1):
			face,nodes,elements,psuedo_nodes = partition_step(d2,d1,path_funct,jump,step,nodes,elements,template,face,psuedo_nodes,nom_el_size = el_step)
			if (z0 == None):
				z0 = path_funct['z'](d2)/1000
				row['layer'] = 0

			if (jump  == True):
				face_elements = list(elements.iloc[-(27):-(27-el_size)].index.copy())
				face_row = {}
				face_row['elements'] = face_elements
				face_row['step'] = i
				face_row['face'] = 'S1'
				face_row['pos'] = 'start'
				face_surfs = face_surfs.append(face_row, ignore_index = True)
				red = False
			jump = False
		else:
			#creates a surface for the recently extruded filament
			jump = True
			if (jump and (red != True)):
				face_elements = list(elements.iloc[-(el_size+1):-1].index.copy())
				face_row = {}
				face_row['elements'] = face_elements
				face_row['step'] = i
				face_row['face'] = 'S2'
				face_row['pos'] = 'end'
				face_surfs = face_surfs.append(face_row, ignore_index = True)
				red = True

		steps = steps.append(row,ignore_index = True)
		d1 = d2

		#increments the step
		step += 1
	return steps,nodes,elements,psuedo_nodes
