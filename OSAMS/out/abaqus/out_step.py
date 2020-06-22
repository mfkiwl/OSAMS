from .surface_changes import *

def out_step(elements,step_no,steps,BC_changes):
	 
	c_step = steps.iloc[step_no]
	dt = c_step['dt'] 
	#HEADER FOR STEP DEFINITION BUILD 
	#PLATE BOUNDRY CONDITIONS ENFORCED
	s_out = f"""
*STEP,NAME = STEP_{step_no}, INC= 20000, NLGEOM = YES
*COUPLED TEMPERATURE-DISPLACEMENT,DELTMX = 10., CETOL= 1e-3
0, {dt}, 1e-9,{dt}
**SOLUTION TECHNIQUE, TYPE = {steps.at[step_no,'SOL_T']}
*BOUNDARY, TYPE = DISPLACEMENT
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3 
"""
	if (steps.iloc[step_no]['type']):
		es = f"*MODEL CHANGE, ADD = STRAIN FREE \nE_STEP_{step_no}\n"
		s_out = s_out + es
#	for i in range(1,step_no):
#		es = es + f",\nE_STEP_{i}"

	#list of boundry condition changes for this step
	changes = BC_changes.loc[BC_changes['step'] == step_no]
	for i,row in changes.iterrows():
		#gets the name of the surface where the change occurs 
		d_step = row['d_step']
		side = row['side']
		j = surf_cond(d_step,side,row['change'])
		s_out = s_out + j

	s_out = s_out + """*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE OUTPUT, NSET = N2
U
*END STEP
"""
	return s_out
