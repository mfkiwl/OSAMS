import numpy as np
import pandas as pd


	
"""
generates the INP lines to change the conditions for a surface
args:
	step:	what deposition step was the materiel that the surface belongs to deposited?
	side:	what side is the surface on (UP DOWN LEFT RIGHT)
	cond:	what BC category the surface will have
BC CATS:
	free_surface:	natural convection + radiation
	hot_surface:	forced convection
	bond:			bond surface no heat transfer with the enviroment
"""
def surf_cond(step,side,cond):
	s_def = f"*SFILM\n{side}_{step}, F,"
	print(side)

	if (cond == "free_surface"):
		#sink temperature and convection cooefficent
		fs_temp = 20.0
		fs_h = 67 
		s_def = s_def + (f" {fs_temp}, {fs_h}\n")
		#radiation goes here

	elif (cond == "hot_surface"):
		#sink temperature and convection cooefficent
		hs_temp = 20.0
		hs_h = 67
		s_def = s_def + (f" {hs_temp}, {hs_h}\n")
		#radiation goes here

	elif (cond == "bond"):
		#sink temperature and convection cooefficent
		fs_temp = 20
		fs_h = 0.0 
		s_def = s_def + (f" {fs_temp}, {fs_h}\n")
		#radiation goes here
	return s_def
		
