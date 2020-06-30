import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np 
import itertools
import template
import time
sys.path.append("G:\My Drive\PYthon\PROCESSMESH\FDMSIM")
import OSAMS
from OSAMS.out.abaqus import *

pot = plt.figure().gca(projection='3d')
feed = 60

fw = 0.3
fh = 0.3

len_fil = 200
wid_fil = 100
l = fw * len_fil
w = fw * wid_fil

area_size = 4
a_d = area_size * fw

layers = 2 

#APPLY SERVICE LOAD?
service = True


g_code = """;TEST
;*****INITIALIZE MACHINE******
M104 T200
M106 F100
M140 T60
"""
t = (l-a_d)/feed
t0 = [t, (t/2) + (l*(wid_fil-area_size))/(2 * feed)]
t = (w-a_d)/feed
t90 = [t, (t/2) + (w*(len_fil-area_size))/(2 * feed)]
deg90 = False
for i in range(0,layers):
	#first filament
	pos = True
	l0 = f"G4 S{t0[1]}\n"
	of = "G7 X0 Y0\n"
	if (deg90):
		l0 = f"G4 S{t90[1]}\n"
		of = "G7 X0.15 Y-0.15\n"
	l1 = f"G0 X0 Y0 F{feed}\n"
	#g_code += (l0)
	g_code += of
	g_code += (l1)
	for j in range(0,area_size):
		x = pos*fw*area_size*2
		y = j * fw
		wait = t0[1]
		if (deg90):
			x,y  = y,x
			wait = t90[1]
		line = f"G1 X{x} Y{y}\n"
		g_code += (line)
		if (i!=area_size-1):
			ws = f"G4 S{wait}\n"
			g_code += (ws)

		#next filament
		line = f"G0 X{x} Y{y+fw}\n"
		if (deg90):
			line = f"G0 X{x+fw} Y{y}\n"

		g_code += (line)
		pos^=True
	
	#REST OF THE PLATE
	l0 = f"G4 S{t0[1]}\n"
	if (deg90):
		l0 = f"G4 S{t90[1]}\n"
	
	#g_code += (l0)
	g_code += f"G0 X0 Y0 Z{(i+1)*fh}\n"
	#deg90 ^= True

path_states = OSAMS.interpreter.read_path(g_code)
pot.plot3D(path_states['x'],path_states['y'],path_states['z'],linestyle = 'dashed')

#partitions the toolpath into steps
step_partitions = OSAMS.partititon.partition_steps(path_states,nominal_step = 0.33)

path_functs = OSAMS.partititon.df_functs(path_states,'time')

start = time.time()
#gets the template (9Brick)
cn = template.nodes[['type','ref','x','y','z','step','up','down','left','right']]
input("WAIT")
brick = {}
brick['nodes'] = template.nodes
brick['elements'] = template.elements
brick['width'] = 0.0003
nodes= cn[0:0].copy()
elements = template.elements[0:0].copy()

#global properties (placeholder)
model = {}
model['enclosure'] = 20 
model['emissivity'] = 0.3
model['plate'] = 210
model['h_nat'] = 67
model['h_fan'] = 67 

#extrudes the mesh and the template
steps,nodes,elements,p_nodes = OSAMS.manufacture.create_steps(step_partitions,path_functs,nodes,elements,brick)
input('wait')
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
"""
for i in steps.index:
	sn = p_nodes.loc[p_nodes['step'] == i].copy()
	pot.scatter(sn['x']*1000,sn['y']*1000,sn['z']*1000,s = 20)
pot.set_xlim(0,1)
pot.set_zlim(-0.5,0.5)
pot.set_ylim(0,1)
pot.set_xlabel('x(mm)')
pot.set_ylabel('y(mm)')
pot.set_zlabel('z(mm)')
"""
#
BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))
BC_changes = BC_changes[BC_changes['side'] != 'NO']

#build surface is redundant
mask = (steps['layer'] == 0)&( steps['type'] == 1)
layer1_steps = steps.loc[mask].index
for i in layer1_steps:
	surfaces.loc[i,'DOWN'] = 1

inp_file = open('../teal.inp','w+')
gen_inp = lambda x: inp_file.write(x)

#flags the build plate nodes
nodes = OSAMS.analyze.build_nodes(nodes)
gen_inp(out_nodes(nodes))
gen_inp(out_elements(elements,nodes))
gen_inp(OSAMS.material.def_mat.materiel_model())
gen_inp(OSAMS.material.def_mat.section())
gen_inp(build_surf(elements,steps))
gen_inp(element_sets(elements,steps))
gen_inp(node_sets(nodes,"BUILD_PLATE"))
gen_inp(out_surf(elements,surfaces))
print(nodes.shape[0])
num_step = steps.shape[0]

gen_inp(inital_step(elements,num_step,steps,surfaces,model))
for i in range(1,num_step):
	gen_inp(out_step(elements,i,steps,BC_changes,model))

#applies the service load as described in service .inp
if (service):
	service_step = open('service.inp').read()
	gen_inp(service_step)
end = time.time()
print(end-start)
