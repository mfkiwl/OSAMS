from .surface_changes import *
def thermal_step(elements,step_no,steps,BC_changes,model):
	
	#LUMPING STEPS TOGETHER
	#HEADER FOR STEP DEFINITION BUILD 
	#PLATE BOUNDRY CONDITIONS ENFORCED
	c_step = steps.iloc[step_no]
	dt = c_step['dt']
	s_out = f"""
*STEP,NAME = STEP_{step_no}, INC= 20000
*HEAT TRANSFER, DELTMX = 10.
{min([0.01,dt])}, {dt}, 1e-9, {dt}
*CONTROLS, ANALYSIS=DISCONTINUOUS
"""
	if (steps.iloc[step_no]['type']):
		es = f"*MODEL CHANGE, ADD = STRAIN FREE \nE_STEP_{step_no}\n"
		#FOR ALTERNATE Heat addition
		if model['A_TEMP']:
			ef =f"*DFLUX, OP = NEW, AMPLITUDE = QADD\n"
			print(model['e_time'])
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

	s_out = s_out + """*OUTPUT, FIELD, VARIABLE = PRESELECT, NUMBER INTERVAL = 1
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE FILE, NSET=ALLNODES, FREQUENCY = 10
NT
*OUTPUT, FIELD
*NODE OUTPUT, NSET=ALLNODES
*END STEP
"""
	return s_out
