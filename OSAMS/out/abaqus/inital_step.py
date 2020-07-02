def inital_step(elements,num_step,steps,surfaces,model):
	temp = model['plate']
	c_step = steps.loc[0]
	dt = c_step['dt'] 
	s_out = f"""
*INITIAL CONDITIONS, TYPE = TEMPERATURE
ALLNODES, 200.
**INITIAL CONDITIONS, TYPE = TEMPERATURE
**BUILD_PLATE, 60.
*NSET, NSET = N2
2
*SURFACE, NAME = FREE_SURFACE, TYPE = ELEMENT
ALLELEMENTS,
*STEP,NAME = STEP_0, INC= 20000, NLGEOM = YES
*COUPLED TEMPERATURE-DISPLACEMENT, DELTMX = 10., CETOL= 1e-3
{min([0.01,dt])}, {dt}, 1e-9, {dt}
**SOLUTION TECHNIQUE, TYPE = {steps.at[0,'SOL_T']}
*BOUNDARY, TYPE = DISPLACEMENT
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3 
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
	if (steps.at[0,'type'] == 1):
		es = es + f"""
*DFLUX
E_STEP_0,BF, {(2020*1040)*(200-20)/dt}
"""
		
	
	#COMMITS setting all freee surface
	s_out = s_out + es

	s_out = s_out + f"""
*SFILM
BUILD_SURFACE, F, {c_step['BP_T']}, {model['plate']}
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE OUTPUT, NSET = N2
U
*END STEP
"""
	return s_out
