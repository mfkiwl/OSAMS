import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import FDMSIM as osams
import itertools
import template
from FDMSIM.out.abaqus import *
with open('laminate.gcode', 'r') as myfile:
  gcode = myfile.read()

path_states = osams.interpriter.read_path(gcode)


#partitions the toolpath into steps
step_partitions = osams.partititon.partition_steps(path_states,nominal_step = 10)
print(step_partitions)

path_functs = osams.partititon.df_functs(path_states,'time')

#partitions the extrusion steps

plt.plot(path_states['time'],path_states['temp'])
plt.show()
#gets the template (9Brick)
cn = template.nodes[['type','ref','X','step','master']]
brick = {}
brick['nodes'] = template.nodes
brick['elements'] = template.elements
nodes= cn[0:0].copy()
elements = template.elements[0:0].copy()

#extrudes the mesh and the template
steps,nodes,elements = osams.manufacture.create_steps(step_partitions,path_functs,nodes,elements,brick)

#where is extrusion happening
extrusion_steps = steps.loc[steps['type'] == 1]
extrusion_steps = extrusion_steps.index 
#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','d_step','side','change']
BC_changes = pd.DataFrame(columns = cols)

indx = list(itertools.product(extrusion_steps,['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['ref']
surfaces = pd.DataFrame(index = idx,columns = surf_cols)
surfaces['ref'] = -1

print('onto node merging')
for i in extrusion_steps:
	(nodes,elements, surfaces, BC_changes) = osams.analyze.analysis_step(nodes,elements,surfaces,BC_changes,i)
	print('LAYER DONE')


#drops duplicate boundry condition changes
BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))
BC_changes = BC_changes[BC_changes['side'] != 'NO']

inp_file = open('analysis.inp','w+')
gen_inp = lambda x: inp_file.write(x)

#flags the build plate nodes
nodes = osams.analyze.build_nodes(nodes)
gen_inp(out_nodes(nodes))
gen_inp(out_elements(elements,nodes))
gen_inp(osams.material.def_mat.materiel_model())
gen_inp(osams.material.def_mat.section())
gen_inp(build_surf(elements,steps))
gen_inp(element_sets(elements,steps))
gen_inp(node_sets(nodes,"BUILD_PLATE"))
gen_inp(out_surf(elements,surfaces))

num_step = steps.shape[0]
gen_inp(inital_step(elements,num_step,steps,surfaces))
for i in range(1,num_step):
	gen_inp(out_step(elements,i,steps,BC_changes))
