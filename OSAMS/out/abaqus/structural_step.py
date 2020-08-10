
def structural_step(elements,step_no,steps,job_name,a_step):
	s_out = ""	 
	c_step = steps.iloc[step_no-1]
	dt = c_step['dt'] 
	#HEADER FOR STEP DEFINITION BUILD 
	#PLATE BOUNDRY CONDITIONS ENFORCED
	s_out = f"""
*STEP,NAME = STEP_{step_no}, INC= 20000, NLGEOM = YES
*STATIC
*TEMPERATURE,FILE={job_name}, BSTEP={a_step}
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


	s_out = s_out + """*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT, NUMBER INTERVAL = 1 
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
"""
	return s_out
