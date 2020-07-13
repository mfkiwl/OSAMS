from .surface_changes import *
def thermal_step(elements,step_no,steps,BC_changes,model):
	 
	c_step = steps.iloc[step_no]
	dt = c_step['dt'] 
	#HEADER FOR STEP DEFINITION BUILD 
	#PLATE BOUNDRY CONDITIONS ENFORCED
	s_out = f"""
*STEP,NAME = STEP_{step_no}, INC= 20000
*HEAT TRANSFER, DELTMX = 10.
{min([0.01,dt])}, {dt}, 1e-9, {dt}
**SOLUTION TECHNIQUE, TYPE = {steps.at[step_no,'SOL_T']}
"""
	if (steps.iloc[step_no]['type']):
		es = f"*MODEL CHANGE, ADD = STRAIN FREE \nE_STEP_{step_no}\n"
		#FOR ALTERNATE Heat addition
		if model['A_TEMP']:
			ef =f"*DFLUX, OP = NEW, AMPLITUDE = QADD\n"
			ef += f"E_STEP_{step_no}, BF, {model['t_mass']*(model['extruder'] - model['enclosure'])/model['e_time']}\n"
		es = es + ef
		s_out = s_out + es

	#list of boundry condition changes for this step
	changes = BC_changes.loc[BC_changes['step'] == step_no]
	for i,row in changes.iterrows():
		#gets the name of the surface where the change occurs 
		d_step = row['d_step']
		side = row['side']
		j = surf_cond(d_step,side,row['change'],model)
		s_out = s_out + j

	s_out = s_out + """**OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE FILE, NSET=ALLNODES, FREQUENCY = 1
NT
*OUTPUT, FIELD
*NODE OUTPUT, NSET=ALLNODES
*END STEP
"""
	return s_out
