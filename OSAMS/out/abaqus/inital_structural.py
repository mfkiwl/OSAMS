def inital_structural(elements,num_step,steps,surfaces,model,job_name,n_step):
	s_out = f"""
*STEP,NAME = STEP_0, INC= 20000, NLGEOM = YES
*STATIC, NLGEOM=YES
*TEMPERATURE,FILE={job_name}, BSTEP=1
*BOUNDARY, TYPE = DISPLACEMENT
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3 
"""
	#removes elements
	es = "*MODEL CHANGE, REMOVE\n"
	for i in range(1,num_step):
		if (steps.at[i,'type'] == 1):
			es = es + f"E_STEP_{i},\n"
	
	s_out = s_out + es

	#sets all surfaces to be free surfaces

	s_out = s_out + f"""
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
"""
	return s_out
