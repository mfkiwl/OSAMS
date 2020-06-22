
"""
outputs the node sets
args:
	nodes:	nodes of the surface
	name:	name of the nodes where this belongs to 
"""
def node_sets(nodes,name,step = 10000):	
	s_def = f"\n*NSET, NSET = {name}\n"
	cn = nodes.loc[nodes['type'] == name]
	#s_def = s_def + f"\n{nodes.index[0]+1}"
	for i,node in cn.iterrows():
		s_def = s_def + f"{i+1},\n"
	#s_def.join("\n")
	return s_def
