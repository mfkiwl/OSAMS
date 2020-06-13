import pandas as pd
import numpy as np

from recalc_surf import *

def out_step(elements,step_no,steps,BC_changes,deposition = True):
	 
	c_step = steps.loc[step_no]
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
	if (deposition):
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

	#ACTIVATES THE ELEMENT SETS FOR THIS SET

def inital_step(elements,num_step,steps,surfaces):
	temp = steps.at[0,'BP_T']
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
0, {dt}, 1e-9,{dt}
**SOLUTION TECHNIQUE, TYPE = {steps.at[0,'SOL_T']}
*BOUNDARY, TYPE = DISPLACEMENT
BUILD_PLATE, 1, 1 
BUILD_PLATE, 2, 2 
BUILD_PLATE, 3, 3 
**BUILD_PLATE,11,11, {temp}
*SFILM
FREE_SURFACE, F, 20, 67
"""
	es = "*MODEL CHANGE, REMOVE\n"
	for i in range(1,num_step):
		if (steps.at[i,'TYPE'] == 'DEPOSITION'):
			es = es + f"E_STEP_{i},\n"
	
	s_out = s_out + es

	#sets all surfaces to be free surfaces
	es = "*SFILM"
	for i,row in surfaces.iterrows():
		if (row['ref'] == -1):
			es = es + f"\n{i[1]}_{i[0]}, F, {20}, {67}"
		
	s_out = s_out + f"""
*SFILM
BUILD_SURFACE, F, {temp}, 210 
*RESTART, WRITE, FREQUENCY = 0
*OUTPUT, FIELD, VARIABLE = PRESELECT
*OUTPUT, HISTORY, VARIABLE = PRESELECT
*NODE OUTPUT, NSET = N2
U
*END STEP
"""
	return s_out
