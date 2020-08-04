def inital_thermal(elements,num_step,steps,surfaces,model):
	temp = model['plate']
	c_step = steps.loc[0]
	IT = model['extruder']
	if model['A_TEMP']:
		IT = model['enclosure']
	dt = c_step['dt'] 
	s_out = f"""
*INITIAL CONDITIONS, TYPE = TEMPERATURE
ALLNODES, {IT}.
*AMPLITUDE, NAME=QADD, VALUE=RELATIVE, DEFINITION=TABULAR, TIME = STEP TIME
0, 1
{model['e_time']},1
{model['e_time']*1.001},0
*SURFACE, NAME = FREE_SURFACE, TYPE = ELEMENT
ALLELEMENTS,
*STEP,NAME = STEP_0, INC= 20000
*HEAT TRANSFER, DELTMX = 10.
{min([0.01,dt])}, {dt}, 1e-9, {dt}
**BUILD_PLATE,11,11, {temp}
"""
	#removes elements
	es = "*MODEL CHANGE, REMOVE\n"
	for i in range(1,num_step):
		if (steps.at[i,'type'] == 1):
			es = es + f"E_STEP_{i},\n"

	
	s_out = s_out + es

	#sets all surfaces to be free surfaces
	es = "*SFILM"
	#print(surfaces)
	for i,row in surfaces.iterrows():
		if (row['ref'] == -1):
			es = es + f"\n{i[1]}_{i[0]}, F, {model['enclosure']}, {model['h_nat']}"
	#COMMITS setting all freee surface
	s_out = s_out + es

	s_out = s_out + f"""
*SFILM
BUILD_SURFACE, F, {model['plate']}, {model['h_plate']}
**DATA FOR THE STRUCTURAL ANALYSIS
*NODE FILE, NSET=ALLNODES, FREQUENCY = 10
NT
*OUTPUT, FIELD
*NODE OUTPUT, NSET=ALLNODES
*OUTPUT, FIELD, VARIABLE = PRESELECT, TIME INTERVAL = 1 
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
"""
	return s_out
