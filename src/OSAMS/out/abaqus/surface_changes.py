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
def surf_cond(step,side,cond,model):
	s_def = f"*SFILM\n{side}_{step}, F,"
	r_def = f"*SRADIATE\n{side}_{step}, R,"

	if (cond == "free_surface"):
		#sink temperature and convection cooefficent and emissivity of the 
		fs_temp = model['enclosure']
		fs_h = model['h_nat']
		fs_r = model['emissivity']
		s_def = s_def + (f" {fs_temp}, {fs_h}\n")
		r_def = r_def + (f" {fs_temp}, {fs_r}\n") 
		#radiation goes here

	elif (cond == "hot_surface"):
		#sink temperature and convection cooefficen
		hs_temp = model['enclosure']
		hs_h = model['h_fan']
		fs_r = model['emissivity']
		s_def = s_def + (f" {hs_temp}, {hs_h}\n")
		r_def = r_def + (f" {hs_temp}, {fs_r}\n") 
		#radiation goes here

	elif (cond == "bond"):
		#sink temperature and convection cooefficent
		fs_temp = 20
		fs_h = 0.0 
		fs_r = 0.0
		s_def = s_def + (f" {fs_temp}, {fs_h}\n")
		r_def = r_def + (f" {fs_temp}, {fs_r}\n") 
		#radiation goes here
	
	#radiation
	s_def = s_def + r_def
	return s_def
		
