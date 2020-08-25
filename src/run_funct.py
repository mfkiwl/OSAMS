'''
this piece of code is the function that runs OSAMS for the default (FDM) analysis procedure used for both the GUI and command line interfaces
CHANGES
DATE		AUTHOR		CHANGE
2020.08.24	Chris Bock	none
2020.8.24	Chris Bock	Mades finding bottom nodes more robust
2020.8.20	Chris Bock	none
'''
#import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np 
import itertools
#import template
import time
sys.path.append("G:\My Drive\PYthon\PROCESSMESH\FDMSIM")
import OSAMS
import service
from OSAMS.out.abaqus import *
from OSAMS.mesh import template
import shutil
import os


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
def OSAMS_RUN(i_file,out_dir,job_name,g_file = 'N/A',template_path = 'N/A'):
	serv = True 
	log = ''

	#i_file = 'EXAMPLE.inp'
	r_file = 'CHANGE_FILE.inp'
	try:
		os.remove(r_file)
	except:
		pass
	shutil.copy(i_file,r_file)

	#job_name = OSAMS.out.read_string(r_file,'JOB_NAME')
	#inp_template = 'inp_plate.inp'
	thermal_job = f'{job_name}_therm' 
	structural_job = f'{job_name}_disp' 
	thermal_file = f'{out_dir}\{thermal_job}.inp'
	structural_file = f'{out_dir}\{structural_job}.inp'
	if (out_dir == 'N/A'):
		thermal_file = f'{thermal_job}.inp'
		structural_file = f'{structural_job}.inp'

	try:
		os.remove(thermal_file)
	except:
		pass
	try:
		os.remove(structural_file)
	except:
		pass

	#TURNS GCODE into tool functions
	if (g_file == 'N/A'):
		g_file = OSAMS.out.read_string(r_file,'GCODE')
	g_code = open(g_file,'r').read()
	path_states = OSAMS.interpreter.read_path(g_code)

	del_t = OSAMS.out.read_data(r_file,'del_t')
	e_step = OSAMS.out.read_data(r_file,'el_step')
	step_partitions = OSAMS.partititon.partition_steps(path_states,nominal_step = del_t)
	path_functs = OSAMS.partititon.df_functs(path_states,'time')
	print(len(step_partitions))



	#gets the template 
	brick = {}
	if (template_path == 'N/A'):
		template_path = OSAMS.out.read_string(r_file,'template')
	f_w = OSAMS.out.read_data(r_file,'bead_width')
	f_h = OSAMS.out.read_data(r_file,'bead_height')
	brick['width'] = f_w
	if (template_path != 0.0):
		tpl = template(f_w,f_h,template = f'{template_path}')
	else:
		tpl = template(f_w,f_h)


	#creates the mesh template
	brick['height'] = f_h 
	brick['nodes'] = tpl.nodes
	brick['elements'] = tpl.elements
	brick['e_type'] = tpl.e_type
	cn = tpl.nodes[['type','ref','x','y','z','step','up','down','left','right']]
	nodes= cn[0:0].copy()
	elements = tpl.elements[0:0].copy()

	#MODEL properties
	model = {}
	model['extruder'] = OSAMS.out.read_data(r_file,'extruder_temp')
	model['enclosure'] = OSAMS.out.read_data(r_file,'enclosure_temp')
	model['emissivity'] = OSAMS.out.read_data(r_file,'emissivity')
	model['plate'] = OSAMS.out.read_data(r_file,'plate_temp')
	model['h_nat'] = OSAMS.out.read_data(r_file,'h_nat')
	model['h_plate'] = OSAMS.out.read_data(r_file,'h_plate')		#Heat transfer coeffcient for build plate
	model['A_TEMP'] = False
	model['A_TEMP'] = bool(OSAMS.out.read_data(r_file,'flux'))
	model['t_mass'] = 1.0
	model['e_time'] = 1.0
	if (model['A_TEMP']):
		model['t_mass'] = OSAMS.out.read_data(r_file,'thermal_density')
		model['e_time'] = OSAMS.out.read_data(r_file,'t_flux')


	#print(len(step_partitions))
	steps,nodes,elements,p_nodes = OSAMS.manufacture.create_steps(step_partitions,path_functs,nodes,elements,brick,el_step = e_step)
	print(steps.shape[0])
	print(steps['layer'])
	nodes['ref'] = nodes.index
	log = log + (f'NUMBER OF PRE MERGE NODES: {nodes.shape[0]}\n')
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
	log = log + (f'NUMBER OF POST MERGE NODES: {nodes.shape[0]}\n')
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
	steps['plate'] = (steps['layer'] == 0)&( steps['type'] == 1)
	layer1_steps = steps.loc[steps['plate']].index

	for i in layer1_steps:
		surfaces.loc[i,'DOWN'] = 1
	num_step = steps.shape[0]
	time.sleep(0.2)
	shutil.copy(r_file,thermal_file)
	shutil.copy(r_file,structural_file)
	time.sleep(0.2)
	#GENERATES THE FILES

	try:
		os.remove(r_file) 
	except:
		pass
	#print(nodes)
	#flags the build plate nodes
	#nodes = OSAMS.analyze.build_nodes(nodes)
	OSAMS.out.exclude_section(thermal_file,'STRUCTURAL')
	OSAMS.out.exclude_section(structural_file,'THERMAL')


	#creates the build surface nodes
	bs_nodes = nodes.loc[nodes['z'] < nodes['z'].min() + 0.00001]
	#finds the left nodes
	max_x = bs_nodes['x'].max() - 0.000001
	min_x = bs_nodes['x'].min() + 0.000001


	front_nodes = bs_nodes.loc[(bs_nodes['x'] > max_x)]
	front_left = front_nodes['y'].idxmax()
	front_right = front_nodes['y'].idxmin()

	rear_nodes = bs_nodes.loc[(bs_nodes['x'] < min_x )]
	rear_left = rear_nodes['y'].idxmax()

	OSAMS.out.ins_tag(thermal_file,'EL_SETS',element_sets(elements,steps))
	OSAMS.out.ins_tag(structural_file,'EL_SETS',element_sets(elements,steps))
	#(build_surf(elements,steps))
	#structural_inp(element_sets(elements,steps))
	OSAMS.out.ins_tag(structural_file,'N_SETS',node_sets(bs_nodes,"BUILD_PLATE"))
	OSAMS.out.ins_tag(thermal_file,'N_SETS',node_sets(bs_nodes,"BUILD_PLATE"))
	surf_txt = out_surf(elements,surfaces) + build_surf(elements,steps)
	OSAMS.out.ins_tag(thermal_file,'SURFACES',surf_txt)
	OSAMS.out.ins_tag(structural_file,'SURFACES',surf_txt)
	#print(nodes.shape[0])

	log = log + (f'NUMBER OF STEPS: {steps.shape[0]}')
	thermal_steps = inital_thermal(elements,num_step,steps,surfaces,model) + '\n'
	structural_steps = inital_structural(elements,num_step,steps,surfaces,model,thermal_job,1) + '\n'
	j = 1
	for i in range(1,num_step):
		thermal_steps += thermal_step(elements,i,steps,BC_changes,model) + '\n'
		structural_steps += (structural_step(elements,i,steps,thermal_job,j)) + '\n'
		j = j + 1

	#applies the service load as described in service .inp
	OSAMS.out.ins_tag(thermal_file,'STEPS',thermal_steps)
	OSAMS.out.ins_tag(structural_file,'STEPS',structural_steps)
	if (serv):
		OSAMS.out.ins_tag(thermal_file,'SERVICE',service.thermal_service())
		struct_serv = service.struct_service(6,front_right,front_left,rear_left,j,thermal_job)
		OSAMS.out.ins_tag(structural_file,'SERVICE',struct_serv)	
	#end = time.time()
	#print(end-start)

	#IF NODES GO AT THE END LESS OVERHEAD
	OSAMS.out.ins_tag(thermal_file,'NODES',out_nodes(nodes))
	OSAMS.out.ins_tag(structural_file,'NODES',out_nodes(nodes))
	OSAMS.out.ins_tag(thermal_file,'ELEMENTS',out_elements(elements,nodes,tpl,analysis_type = 'T'))
	OSAMS.out.ins_tag(structural_file,'ELEMENTS',out_elements(elements,nodes,tpl,analysis_type = 'S'))
	return log
