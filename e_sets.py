import pandas as pd

"""
CREATES THE ELEMENT SET DEFINITIONS FOR THE INP FILE
ARGS:
	ELEMENTS:	dataframe of elements
	step_nums:	the step indices to have sets made
"""
def element_sets(elements,step_nums):
	esets = "\n**ELEMENTS BY DEPOSISTION STEP"
	for i in step_nums:
		#SELECTS ELEMENTS DEPOSITED FOR THAT STEP
		step_elements = elements.loc[elements['step'] == i]

		#HEADER AND FIRST ELEMENT
		es_def = f"\n*ELSET, ELSET = E_STEP_{i}"
		es_def = es_def + f"\n{step_elements.index[0]+1}"

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
	el_def = "*ELEMENT,ELSET = ALLELEMENTS, TYPE = C3D6T"
	elements = elements.loc[elements['step'] < step]
	for i,element in elements.iterrows():
		e_nodes = element.loc[['n1','n2' ,'n3','n4','n5','n6']]
		for e_node in e_nodes:
			if (nodes.at[i,'ref'] != -1):
				e_node = nodes.at[i,'ref']
		el_def = el_def + (f"\n{i+1}\t,{e_nodes[0]}\t,{e_nodes[1]}\t,{e_nodes[2]}\t,{e_nodes[3]}\t,{e_nodes[4]}\t,{e_nodes[5]}")
	return el_def

"""
formats a surface for applying interactions
args:
	nodes:	nodes of the surface
	name:	name of the nodes where this belongs to 
"""
def out_surf(nodes,name,step =  100000):
	s_def = f"\n*SURFACE, NAME = {name}, TYPE=ELEMENT"
	s_def = s_def + f"\nALLELEMENTS,"
	cn = nodes.loc[nodes['type'] == name]
	#s_def = s_def + f"\n{nodes.index[0]+1}"
	#for i,node in cn[1:].iterrows():

		#s_def = s_def + f",\n{i+1}"
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
