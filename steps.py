import pandas as pd
import numpy as np


def out_step(elements,step_no,steps):
	dt = 1
	temp = steps.at[step_no,'BP_T']

	#HEADER FOR STEP DEFINITION BUILD 
	#PLATE BOUNDRY CONDITIONS ENFORCED
	s_out = f"""
*STEP,NAME = STEP_{step_no}, INC= 20000, NLGEOM = YES
*COUPLED TEMPERATURE-DISPLACEMENT,DELTMX = 2., CETOL= 1e-5
0, 1, 1e-9,0.1
**SOLUTION TECHNIQUE, TYPE = {steps.at[step_no,'SOL_T']}
*BOUNDARY, TYPE = DISPLACEMENT
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3 
**BUILD_PLATE,11,11, {temp}
"""
	deposition = True
	if (deposition):
		es = f"*MODEL CHANGE, ADD = STRAIN FREE \nE_STEP_{step_no}"
#	for i in range(1,step_no):
#		es = es + f",\nE_STEP_{i}"
	s_out = s_out + es
	s_out = s_out + """
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
"""
	return s_out

	#ACTIVATES THE ELEMENT SETS FOR THIS SET

def inital_step(elements,num_step,steps):
	temp = steps.at[0,'BP_T']
	s_out = f"""
*INITIAL CONDITIONS, TYPE = TEMPERATURE
ALLNODES, 150.
**INITIAL CONDITIONS, TYPE = TEMPERATURE
**BUILD_PLATE, 60.
*SURFACE, NAME = FREE_SURFACE, TYPE = ELEMENT
ALLELEMENTS,
*STEP,NAME = STEP_0, INC= 20000, NLGEOM = YES
*COUPLED TEMPERATURE-DISPLACEMENT, DELTMX = 2., CETOL= 1e-5
0, 1, 1e-9,0.1
**SOLUTION TECHNIQUE, TYPE = {steps.at[0,'SOL_T']}
*BOUNDARY
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3  
**BUILD_PLATE,11,11, {temp}
*SFILM
FREE_SURFACE, F, 40, 20
*SFILM
BUILD_SURFACE, F, 60.0, 1e6 
"""
	es = "*MODEL CHANGE, REMOVE\n"
	for i in range(1,num_step):
		es = es + f"E_STEP_{i},\n"
	s_out = s_out + es
	s_out = s_out + """
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*END STEP
"""
	return s_out
