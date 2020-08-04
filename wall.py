import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np 
import itertools
import template
import time
sys.path.append("G:\My Drive\PYthon\PROCESSMESH\FDMSIM")
import OSAMS
import service
from OSAMS.out.abaqus import *


pot = plt.figure().gca(projection='3d')
feed = 80 

fw = 10.0
fh = 4.064

wall_length = 1.542e3


layers = 20 

#APPLY SERVICE LOAD?
serv = True


g_code = """;TEST
;*****INITIALIZE MACHINE******
M104 T200
M106 F100
M140 T75
G0 X0 Y0 Z0 F4800
"""
pos = True
for i in range(0,layers):
	z = i * fh
	g_code += f"G0 Y0 Z{z}\n"
	g_code += f"G1 X{wall_length} Y0 Z{z}\n"
	g_code += f"G0 X{wall_length} Y{fw}\n"
	g_code += f"G1 X0\n"
#g_code = """;TEST
#;*****INITIALIZE MACHINE******
#M104 T200
#M106 F100
#M140 T60
#G4 S1
#G0 X0 Y0 Z0 F60
#G1 X2 Y0 Z0
#G3 X2 Y2 I0 J1
#"""
path_states = OSAMS.interpreter.read_path(g_code)
pot.plot3D(path_states['x'],path_states['y'],path_states['z'],linestyle = 'dashed')

plt.show()
#partitions the toolpath into steps
step_partitions = OSAMS.partititon.partition_steps(path_states,nominal_step = 1000)

path_functs = OSAMS.partititon.df_functs(path_states,'time')

start = time.time()
#gets the template (9Brick)
cn = template.nodes[['type','ref','x','y','z','step','up','down','left','right']]
brick = {}
brick['nodes'] = template.nodes
brick['elements'] = template.elements
brick['width'] = fw/1000 
brick['height'] = fh/1000
nodes= cn[0:0].copy()
elements = template.elements[0:0].copy()

#global properties (placeholder)
model = {}
model['extruder'] = 200 
model['enclosure'] = 18 
model['emissivity'] = 0.87
model['plate'] = 65
model['h_plate'] = 210 
model['h_nat'] = 8.5
model['h_fan'] = 8.5 
model['e_time'] = 0.1
model['A_TEMP'] = False 

#extrudes the mesh and the template
steps,nodes,elements,p_nodes = OSAMS.manufacture.create_steps(step_partitions,path_functs,nodes,elements,brick)
nodes['ref'] = nodes.index
extrusion_steps = steps.loc[steps['type'] == 1]
extrusion_steps = extrusion_steps.index 
#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','d_step','side','change']
BC_changes = pd.DataFrame(columns = cols)

#creates the BC change table and surfaces table( will change) 
indx = list(itertools.product(extrusion_steps,['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['ref']
surfaces = pd.DataFrame(index = idx,columns = surf_cols)
surfaces['ref'] = -1
p_nodes,nodes,elements,surfaces,BC_changes = OSAMS.analyze.merge_p_nodes(p_nodes,nodes,elements,surfaces,BC_changes)
nodes = nodes.loc[nodes['ref'] == nodes.index]
"""
for i in steps.index:
	sn = p_nodes.loc[p_nodes['step'] == i].copy()
	pot.scatter(sn['x']*1000,sn['y']*1000,sn['z']*1000,s = 20)
#pot.set_xlim(0,5)
#pot.set_zlim(-0.5,0.5)
#pot.set_ylim(0,2.5)
pot.set_xlabel('x(mm)')
pot.set_ylabel('y(mm)')
pot.set_zlabel('z(mm)')
plt.show()
"""
BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))
BC_changes = BC_changes[BC_changes['side'] != 'NO']

#build surface is redundant
mask = (steps['layer'] == 0)&( steps['type'] == 1)
layer1_steps = steps.loc[mask].index
for i in layer1_steps:
	surfaces.loc[i,'DOWN'] = 1

prefix = 'WALL'
thermal_job = f'{prefix}_therm' 
structural_job = f'{prefix}_disp' 
thermal_file = open(f'../{thermal_job}.inp','w+')
structural_file = open(f'../{structural_job}.inp','w+')


thermal_inp = lambda x: thermal_file.write(x)
structural_inp = lambda x: structural_file.write(x)

#flags the build plate nodes
nodes = OSAMS.analyze.build_nodes(nodes)
thermal_inp(out_nodes(nodes))
structural_inp(out_nodes(nodes))
thermal_inp(out_elements(elements,nodes,template,analysis_type = 'T'))
structural_inp(out_elements(elements,nodes,template,analysis_type = 'S'))
#creates the build surface nodes
bs_nodes = nodes.loc[nodes['z'] < 0.000001]
#finds the left nodes
max_x = bs_nodes['x'].max() - 0.000001
min_x = bs_nodes['x'].min() + 0.000001


front_nodes = bs_nodes.loc[(bs_nodes['x'] > max_x)]
front_left = front_nodes['y'].idxmax()
front_right = front_nodes['y'].idxmin()

rear_nodes = bs_nodes.loc[(bs_nodes['x'] < min_x )]
rear_left = rear_nodes['y'].idxmax()

structural_inp(OSAMS.material.def_mat.materiel_model())
thermal_inp(OSAMS.material.def_mat.materiel_model())
structural_inp(OSAMS.material.def_mat.section())
thermal_inp(OSAMS.material.def_mat.section())
thermal_inp(element_sets(elements,steps))
thermal_inp(build_surf(elements,steps))
structural_inp(element_sets(elements,steps))
structural_inp(node_sets(bs_nodes,"BUILD_PLATE"))

thermal_inp(out_surf(elements,surfaces))
print(nodes.shape[0])
num_step = steps.shape[0]

thermal_inp(inital_thermal(elements,num_step,steps,surfaces,model))
structural_inp(inital_structural(elements,num_step,steps,surfaces,model,thermal_job,1))
j = 1
print(steps['layer'])
#for i in range(1,num_step):
	#thermal_inp(thermal_step(elements,i,steps,BC_changes,model))
	#structural_inp(structural_step(elements,i,steps,thermal_job,j))
	#j = j + 1
for i in range(0,layers):
	layer_steps = steps.loc[steps['layer']==i].index
	thermal_inp(thermal_step(elements,layer_steps,steps,BC_changes,model))

#applies the service load as described in service .inp
if (serv):
	thermal_inp(service.thermal_service())
	struct_serv = service.struct_service(6,front_right,front_left,rear_left,j,thermal_job)
	structural_inp(struct_serv)
	
#end = time.time()
#print(end-start)
