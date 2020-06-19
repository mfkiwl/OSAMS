import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import analysis_step
from increment import *
import template
import path_divide
import g_code_path
from e_sets import *
import def_mat
import step_out   
import itertools
from check_bc import *
"""
this file is responsible for creating the mesh and the extrusion steps for an analysis
"""
layer_z = 0.3
x_hat = np.array([0,1,0])
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
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
def create_steps(partitions,path_funct):
	
	#initializes step dataframe
	steps = pd.DataFrame(columns = ['BP_T','dt','fan','type','layer','extruder'])
	nodes = template.nodes[['type','ref','X','step','master']].copy()
	nodes = nodes[0:0].copy()
	elements = template.elements[0:0].copy()
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
			face,nodes,elements = partition_step(d2,d1,path_funct,jump,step,nodes,elements,face)
			jump = False
		else:
			jump = True

		steps = steps.append(row,ignore_index = True)
		d1 = d2

		#increments the step
		step += 1
	
	return steps,nodes,elements
"""
paritions_steps:
args:
	d0: toolpath distance at the beginning of the step 
	d1: toolpath distance at the end of the step 
	f: machine state function:
	nom_el_size: nominal element size (mm)
	jump: does a new path need to be created ?
	step: the step being partitioned
"""
def partition_step(d1,d0,f,jump,step,nodes,elements,face_dir,nom_el_size = 4):		#def:
	num = math.ceil((d1-d0)/nom_el_size)

	#partitions from END of the step
	s_part = list(np.linspace(d1,d0,num,endpoint = False))
	ax.scatter(	f['x'](s_part),
				f['y'](s_part),
				f['z'](s_part))
	#coordinate of the tool head at the start of the path
	x0 = np.array([	f['x'](d0),
					f['y'](d0),
					f['z'](d0)])/1000
	
	#if the extruder jumps then create a new pat
	if (jump):
		d_next = s_part[-1]

		#coodinate of the tool head at the end of the element
		x1 = np.array([	f['x'](d_next),
						f['y'](d_next),
						f['z'](d_next)])/1000

		#angle of the toolpath relative to x axis
		direction = angle_between(x_hat,(x1-x0))

		nodes,elements = start_path(nodes,elements,template.nodes,template.elements,
									step,direction,x0,x1)
		x0 = x1
		face_dir = direction
		d0 = d_next
		del s_part[-1]
	#extrudes the rest of the step
	for i in s_part[::-1]:
		d12 = (d0+i)/2
		x12 = np.array([	f['x'](d12),
							f['y'](d12),
							f['z'](d12)])/1000
		x1 = np.array([	f['x'](i),
						f['y'](i),
						f['z'](i)])/1000

		direction = angle_between(x_hat,(x1-x0))

		nodes,elements = mesh_extrude(nodes,elements,template.nodes,template.elements,
										step,face_dir,direction,x0,x12,x1)
		face_dir = direction
		d0 = i
		x0 = x1

	return face_dir,nodes,elements

C1 = """M104 T200
M140 T60
G0 X0 Y0 Z0 F40
G1 X4 Y0 Z0
G1 X8 Y0 Z0
G0 X0 Y0 Z0.3
G1 X4 Y0 Z0.3
G1 X8 Y0 Z0.3
"""
CODE = """M104 T200
M106 F100
M140 T60
G0 X0 Y2 Z0 F20
G3 X0 Y0 Z0 I0 J-1
G1 X5 Y0 Z0 
G3 X5 Y2 Z0 I0 J1
G0 X0 Y2 Z0.3
G3 X0 Y0 Z0.3 I0 J-1
G1 X5 Y0 Z0.3
G3 X5 Y2 Z0.3 I0 J1
"""
CODE2 = """M104 T200
M106 F100 
M140 T60
G0 X0 Y0 Z0 F80 
G1 X0 Y0 Z0
G2 X0 Y0 Z0 I3 J0
G0 Z0.4
G2 X0 Y0 I3 J0
G0 Z0.8
G2 X0 Y0 I3 J0
"""
#Defines the materiel toolpath
tool_path = g_code_path.read_path(CODE)
tool_path.to_csv("pout.csv")
ax.plot3D(tool_path['x'],tool_path['y'],tool_path['z'],color = 'r',linestyle = 'dashed')

#creates tool functions
machine_functs = path_divide.df_functs(tool_path,'time')

#partitions toolpath into different extrusion steps 
partitions = path_divide.partition_steps(tool_path,nominal_step = 6)
ax.scatter(	machine_functs['x'](partitions),
			machine_functs['y'](partitions),
			machine_functs['z'](partitions))
steps,nodes,elements = create_steps(partitions,machine_functs)
ax.set_xlabel('x (mm)')
ax.set_xlim(-1,7)
ax.set_ylim(0,8)
ax.set_zlim(0,3)
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')
plt.show()


#steps where extrusion is happening
extrusion_steps = steps.loc[steps['type'] == 1]
extrusion_steps = extrusion_steps.index 
#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','d_step','side','change']
BC_changes = pd.DataFrame(columns = cols)

#LIST OF SURFACES
#index coloums of table of surfaces
#CREATE THING TO MAKE SURFACE DF

indx = list(itertools.product(extrusion_steps,['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['ref']
surfaces = pd.DataFrame(index = idx,columns = surf_cols)
surfaces['ref'] = -1

#prevents redundant build surface
layer_1_steps = steps.loc[steps['layer'] == 0]
layer_1_steps = layer_1_steps.index
surfaces.loc[(layer_1_steps,'DOWN'),'ref'] = 1

#merges and recalculates BCs for all deposition steps
for i in extrusion_steps:
	(nodes,elements, surfaces, BC_changes) = analysis_step.analysis_step(nodes,elements,surfaces,BC_changes,i)
	print(f"STEP {i} DONE")

BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))
BC_changes = BC_changes[BC_changes['side'] != 'NO']

print(BC_changes)
inp_file = open('analysis.inp','w+')
gen_inp = lambda x: inp_file.write(x)
nodes = dsp(nodes)
gen_inp(out_nodes(nodes))
gen_inp(out_elements(elements,nodes))
gen_inp(def_mat.materiel_model())
gen_inp(def_mat.section())
gen_inp(build_surf(elements,steps))
gen_inp(element_sets(elements,steps))
gen_inp(n_set(nodes,"BUILD_PLATE"))
gen_inp(gen_surf(elements,surfaces))

num_step = steps.shape[0]
gen_inp(step_out.inital_step(elements,num_step,steps,surfaces))
for i in range(1,num_step):
	gen_inp(step_out.out_step(elements,i,steps,BC_changes,surfaces))


#MERGES THE NODES
inp_file.close()
