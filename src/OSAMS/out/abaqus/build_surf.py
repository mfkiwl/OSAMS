"""
defines the build surface of the model
"""
def build_surf(elements,steps):
	build_steps = steps.loc[steps['layer'] == 0]
	build_steps = build_steps.index
	#print("BUILDING STEP")
	#print(build_steps)
	s_def = f"*SURFACE, NAME = BUILD_SURFACE, TYPE=ELEMENT"
	build_elements = elements.loc[elements['step'].isin(build_steps)]
	build_elements = build_elements.loc[build_elements['DOWN'] != 'NO']
	for i,row in build_elements.iterrows():
		s_def = s_def + f"\n {i+1}, {row['DOWN']}"
	return s_def+'\n'
