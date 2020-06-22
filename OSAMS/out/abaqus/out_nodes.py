
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
