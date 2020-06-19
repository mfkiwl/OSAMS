import numpy as np
import pandas as pd
from scipy.interpolate import *
import math
import matplotlib.pyplot as plt
from g_code_path import *

#fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
#layer_z = 0.4

def partition_steps(path,nominal_step = 1000, dev_factor=0):	
	
	#finds places where there is a change in extruder temperature
	f = (path['extruding'].diff(periods = -1) != 0) | (path['extruding'].diff(periods = 1) != 0)
	t = path[['time','extruding']].loc[f].copy() 
	#plt.vlines(t,ymin = 0, ymax = 200)

	
	#find places where nominal step distance is exceeded 
	t = t.drop_duplicates(subset = 'time')
	t['step_time'] = t['time'].diff() 

	#finds places where the step distance in too high
	t['ratio'] = t['step_time']/nominal_step
	long_step = t.loc[t['ratio']>1].copy()
	long_step = long_step.loc[long_step['extruding'] == 1]
	long_step = long_step.loc[long_step['ratio'] != np.nan].copy() 


	for i,row in long_step.iterrows():
		#inserts the new partitions
		partitions = int(math.ceil(row['ratio']))
		dist = row['step_time']/partitions
		for j in range(1,partitions):
			c_dist = row['time'] - j*dist
			t = t.append({"time":c_dist,"step_time":dist,"ratio":0,"extruding":1},ignore_index = True)




	#plt.vlines(t['distance'],linestyle = 'dashed',ymin = 0, ymax = 200)
	#determines disttances between partiation
	t = t['time']
	t = t.sort_values()
	return(t)


"""
df_funct
creates a dictinary of lamda functions that linearly interpolates with respect to x_col
args:
	df:		dataframe to be parametrized
	x_col:	the coloumn containing x values
"""
def df_functs(df,x_col):
	functs = {}
	for i in list(df):
		#linear interpolation between steps 
		functs[i] = interp1d(df[x_col],df[i])
	functs['extruding'] = interp1d(df['time'],df['extruding'],kind = 'next')

	return functs


#CODE = """M104 T200
#M106 F100 
#M140 T60
#G1 X0 Y0 Z0 F80
#G1 X1 Y0 Z0
#G1 X6 Y0 Z0
#G3 X6 Y2 I0 J1
#G2 X6 Y4 I0 J1
#G0 X0 Y0 Z0.4
#G1 X0 Y0 
#G1 X1 Y0 
#G1 X6 Y0 
#G3 X6 Y2 I0 J1
#G2 X6 Y4 I0 J1
#"""
#path = read_path(CODE)
#f = df_functs(path,'distance')
#
#print(path[['time','distance']])
#ax.plot3D(path['x'],path['y'],path['z'],color = 'r',linestyle = 'dashed')
#partitions = path_divide(path)
#partitions = partitions['distance']
#partitions = partitions.sort_values()
#print(partitions)
#ax.set_xlabel('x (mm)')
#ax.set_xlim(0,7)
#ax.set_ylim(0,7)
#ax.set_zlim(0,7)
#ax.set_ylabel('y (mm)')
#ax.set_zlabel('z (mm)')
#ax.scatter(f['x'](partitions),
#			f['y'](partitions),
#			f['z'](partitions))
#
#steps = create_steps(partitions,f)
#print(steps)
#plt.show()

