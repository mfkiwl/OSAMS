e_list = [f"n{i}" for i in range(1,21)]
"""
Outputs the element definitions for use in .INP file
args:
	elements:	dataframe of elements 
	nodes:		dataframe of nodes
"""
def out_elements(elements,nodes,template,analysis_type = 'C',step = 100000):
	
	el_def = f"*ELEMENT,ELSET = ALLELEMENTS, TYPE = {template.e_type['abaqus'].at[analysis_type]}"
	elements = elements.loc[elements['step'] < step]
	for i,element in elements.iterrows():
		e_nodes = element.loc[e_list]+ 1
		el_def = el_def + f"\n{i+1}"
		for j in range(0,20):
			el_def = el_def + f",{e_nodes[j]}"
	return el_def + '\n'
