import pandas as pd

"""
generates the lines in the INP file to generate the surfaces for STEP
args:
	name:	the name of the elements in the surface (down,up...)
	step:	the step to generate surfaces for
"""
def surf_step(elements,name,step):
	surf_elements = elements.loc[elements['step'] == step]
	surf_elements = surf_elements.loc[elements['type'] == name]
	s_out = f"\n*SURFACE, NAME = {name}_{step}, TYPE = ELEMENT"
	for i,element in surf_elements.iterrows():
		s_out = s_out + f'\n{i},'
	return s_out
	
