import pandas as pd
import numpy as np


def out_step(elements,step_no,steps):
	dt = 1
	temp = steps.at[step_no,'BP_T']

	#HEADER FOR STEP DEFINITION BUILD PLATE BOUNDRY CONDITIONS ENFORCED
	s_out = f"""
*STEP,INC= 20000, NLGEOM = YES
COUPLED TEMPERATURE-DISPLACEMENT, CETOL= 1e-5
0, {dt}, 1e-5,0.1
*SOLUTION TECHNIQUE, TYPE = {steps.at[step_no,'SOL_T']}
*BOUNDARY TYPE = DISPLACEMENT
BUILD_PLATE 1,2,3
*BOUNDARY TYPE = TEMPERATURE 
BUILD_PLATE {temp}
"""
	es = "*MODEL CHANGE, ADD = STRAIN FREE \nE_STEP_0"
	for i in range(1,step_no):
		es = es + f",\nE_STEP_{i}"
	s_out = s_out + es
	return s_out

	#ACTIVATES THE ELEMENT SETS FOR THIS SET


