
import re 

#PREVENTS RECOMPILING REGEX
down_check = re.compile('.*DOWN.*')
up_check = re.compile('.*UP.*')
left_check = re.compile('.*LEFT.*')
right_check = re.compile('.*RIGHT.*')
"""
Generates a surfaces based on where elements are in template
args:
	elements: 	dataframe of the elements
	names:		names of category to be in this surface
	name:		name of surface in inp file
returns:
	step surface definitions for the entire domain
"""
def out_surf(elements,surfaces):
	out = ""
	for i,row in surfaces.iterrows():
		#prevents creating resundant surfaces
		if (row['ref'] == -1):
			
			#gets the indexes of the surface
			step = i[0]
			name = i[1]
		
			s_def = f"*SURFACE, NAME = {name}_{step}, TYPE=ELEMENT"

			if (name == 'DOWN'):
				els = elements.loc[elements['type'].apply(lambda x: bool(down_check.match(x)))]
				els = els.loc[els['step']== step]
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
				els = elements.loc[elements['type'].apply(lambda x: bool(right_check.match(x)))]
				els = els.loc[els['step']== step ]
				for i,els in els.iterrows():
					s_def = s_def + f"\n{i+1}, S4"
			out = out + s_def + "\n"
	return out
