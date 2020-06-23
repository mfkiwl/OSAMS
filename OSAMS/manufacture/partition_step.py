import numpy as np
import math
from ..mesh.quad import *

layer_z = 0.3
x_hat = np.array([0,1,0])
def angle_between(v1, v2):
	theta = (np.arctan2(np.cross(v1,v2),np.dot(v1,v2))[2])%(2*np.pi)
	return theta

"""
paritions_steps:
args:
	d0:	time at the start of the step
	d1: time at the end of the step
	f: machine state function
	nom_el_size: nominal element size (mm)
	jump: does a new path need to be created ?
	step: the step being partitioned
	nodes: dataframe of the current nodes
	elements: dataframe of the current elements
	template: dictionary of the template nodes and elements
"""
def partition_step(d1,d0,f,jump,step,nodes,elements,template,face_dir,nom_el_size = 8):		#def:
	num = math.ceil((d1-d0)/nom_el_size)

	#partitions from END of the step
	s_part = list(np.linspace(d1,d0,num,endpoint = False))
	#coordinate of the tool head at the start of the path
	x0 = np.array([	f['x'](d0),
					f['y'](d0),
					f['z'](d0)])/1000
	
	#if the extruder jumps then create a new pat
	if (jump):
		d_next = s_part[-1]

		#coodinate of the tool head at the end of the element
		x1 = np.array([	f['x'](d_next),
						f['y'](d_next),
						f['z'](d_next)])/1000

		#angle of the toolpath relative to x axis
		direction = angle_between(x_hat,(x1-x0))

		nodes,elements = start_path(nodes,elements,template['nodes'],template['elements'],
									step,direction,x0,x1)
		x0 = x1
		face_dir = direction
		d0 = d_next
		del s_part[-1]
	#extrudes the rest of the step
	for i in s_part[::-1]:
		d12 = (d0+i)/2
		x12 = np.array([	f['x'](d12),
							f['y'](d12),
							f['z'](d12)])/1000
		x1 = np.array([	f['x'](i),
						f['y'](i),
						f['z'](i)])/1000

		direction = angle_between(x_hat,(x1-x0))

		nodes,elements = extrude(nodes,elements,template['nodes'],template['elements'],
										step,face_dir,direction,x0,x12,x1)
		face_dir = direction
		d0 = i
		x0 = x1

	return face_dir,nodes,elements
