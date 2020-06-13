import pandas as pd
import re 

#PREVENTS RECOMPILING REGEX
down_check = re.compile('.*DOWN.*')
up_check = re.compile('.*UP.*')
left_check = re.compile('.*LEFT.*')
right_check = re.compile('.*RIGHT.*')
e_list = [f"n{i}" for i in range(1,21)]

"""
CREATES THE ELEMENT SET DEFINITIONS FOR THE INP FILE
ARGS:
	ELEMENTS:	dataframe of elements
	step_nums:	the step indices to have sets made
"""
def element_sets(elements,steps):
	esets = "\n**ELEMENTS BY DEPOSISTION STEP"
	for i,row in steps.iterrows():
		if (row['TYPE'] == 'DEPOSITION'):
			#SELECTS ELEMENTS DEPOSITED FOR THAT STEP
			step_elements = elements.loc[elements['step'] == i]
			#print(step_elements)
			#print("*********************************")

			#HEADER AND FIRST ELEMENT
			es_def = f"\n*ELSET, ELSET = E_STEP_{i}"
			es_def = es_def + f"\n{step_elements.index[0] + 1}"

			for i,row in step_elements[1:].iterrows():
				es_def = es_def + f",\n{i+1}"

			esets = esets + es_def
	#END
	esets.join("\n")
	return esets

"""
out_nodes
args:
	nodes: list of nodes
returns:
	nodes argument to an abaqus input file as a string
"""
def out_nodes(nodes,step = 100000):
	el_def = "*NODE,NSET = ALLNODES\n"
	nodes = nodes.loc[nodes['step'] < step]
	for i,node in nodes.iterrows():
		if (node['ref'] == -1):
			el_def = el_def + (f"{i+1}\t,{node['X'][0]}\t,{node['X'][1]}\t,{node['X'][2]} \n")
	return el_def
			
"""
Outputs the element definitions for use in .INP file
args:
	elements:	dataframe of elements 
	nodes:		dataframe of nodes
"""
def out_elements(elements,nodes,step = 100000):
	el_def = "*ELEMENT,ELSET = ALLELEMENTS, TYPE = C3D20T"
	elements = elements.loc[elements['step'] < step]
	for i,element in elements.iterrows():
		e_nodes = element.loc[e_list]+ 1
		el_def = el_def + f"\n{i+1}"
		for j in range(0,20):
			el_def = el_def + f",{e_nodes[j]}"
	return el_def

"""
formats a surface for applying interactions
args:
	nodes:	nodes of the surface
	name:	name of the nodes where this belongs to 
"""
def out_surf(nodes,name,step =  100000):
	s_def = f"\n*SURFACE, NAME = {name}, TYPE=ELEMENT"
	s_def = s_def + f"\n ALLELEMENTS,"
	cn = nodes.loc[nodes['type'] == name]
	#s_def = s_def + f"\n{nodes.index[0]+1}"
	#for i,node in cn[1:].iterrows():

		#s_def = s_def + f",\n{i+1}"
	return s_def

"""
defines the build surface of the model
"""
def build_surf(elements,steps):
	build_steps = steps.loc[steps['layer'] == 0]
	build_steps = build_steps.index
	#print("BUILDING STEP")
	#print(build_steps)
	s_def = f"\n*SURFACE, NAME = BUILD_SURFACE, TYPE=ELEMENT"
	build_elements = elements.loc[elements['step'].isin(build_steps)]
	for i,row in build_elements.iterrows():
		s_def = s_def + f"\n {i+1},"
	return s_def
		

"""
outputs the node sets
args:
	nodes:	nodes of the surface
	name:	name of the nodes where this belongs to 
"""
def n_set(nodes,name,step = 10000):	
	s_def = f"\n*NSET, NSET = {name}\n"
	cn = nodes.loc[nodes['type'] == name]
	#s_def = s_def + f"\n{nodes.index[0]+1}"
	for i,node in cn.iterrows():
		s_def = s_def + f"{i+1},\n"
	#s_def.join("\n")
	return s_def
1
"""
Generates a surfaces based on where elements are in template
args:
	elements: 	dataframe of the elements
	names:		names of category to be in this surface
	name:		name of surface in inp file
returns:
	surface definitions for the entire domain
"""
def gen_surf(elements,surfaces):
	out = ""
	for i,row in surfaces.iterrows():
		#prevents creating resundant surfaces
		if (row['ref'] == -1):
			
			#gets the indexes of the surface
			step = i[0]
			name = i[1]
		
			s_def = f"\n*SURFACE, NAME = {name}_{step}, TYPE=ELEMENT"

			if (name == 'DOWN'):
				els = elements.loc[elements['type'].apply(lambda x: bool(down_check.match(x)))]
				els = els.loc[els['step']== step ]
				for i,els in els.iterrows():
					s_def = s_def + f"\n{i+1}, S5"
			elif (name == 'UP'):
				els = elements.loc[elements['type'].apply(lambda x: bool(up_check.match(x)))]
				els = els.loc[els['step']== step ]
				for i,els in els.iterrows():
					s_def = s_def + f"\n{i+1}, S3"
			elif (name == 'LEFT'):
				els = elements.loc[elements['type'].apply(lambda x: bool(left_check.match(x)))]
				els = els.loc[els['step']== step ]
				for i,els in els.iterrows():
					s_def = s_def + f"\n{i+1}, S6"
			elif (name == 'RIGHT'):
				els = elements.loc[elements['type'].apply(lambda x: bool(left_check.match(x)))]
				els = els.loc[els['step']== step ]
				for i,els in els.iterrows():
					s_def = s_def + f"\n{i+1}, S4"
			out = out + s_def + "\n"
	return out
