import numpy as np
import math
import pandas as pd
from ..mesh.quad import *

layer_z = 0.3
x_hat = np.array([0,1,0])
BIG_X = np.array([1,0,0])
def angle_between(v1, v2):
	theta = (np.arctan2(np.cross(v1,v2),np.dot(v1,v2))[2])%(2*np.pi)
	return theta

"""
rotates about the GLOBAL z axis
args:
	theta:		angle
returns:
	rotation matrix
"""
def rotZ(theta):
	R = np.array([[np.cos(theta),	-np.sin(theta), 0],
				  [np.sin(theta),	np.cos(theta), 0],
				  [0,0,1]])
	return R

def average_angle(theta1,theta2):
	U1 =  np.array([np.cos(theta1), np.sin(theta1),0])
	U2 =  np.array([np.cos(theta2), np.sin(theta2),0])
	U = (U1+ U2)/2
	return angle_between(BIG_X,U)

def angle_between(v1, v2):
	theta = (np.arctan2(np.cross(v1,v2),np.dot(v1,v2))[2])
	return theta

"""
paritions_steps:
args:
	d0:	time at the start of the step
	d1: time at the end of the step
	f: machine state function
	nom_el_size: nominal element size (mm)
	jump: does a new path need to be created? 
	step: the step being partitioned
	nodes: dataframe of the current nodes
	elements: dataframe of the current elements
	template: dictionary of the template nodes and elements
returns:
	face_dir:	angle of the face at the end of this step
	nodes:		dataframe of nodes
	elements:	dataframe of elements
"""
def partition_step(d1,d0,f,jump,step,nodes,elements,template,face_dir,pseudo_nodes,nom_el_size =0.101):		#def:
	num = math.ceil((d1-d0)/nom_el_size)

	#partitions from END of the step
	s_part = list(np.linspace(d1,d0,num,endpoint = False))
	#coordinate of the tool head at the start of the path
	x0 = np.array([	f['x'](d0),
					f['y'](d0),
					f['z'](d0)])/1000
	d00 = d0
	#if the extruder jumps then create a new path
	
	#creates the psuedonodes for this step
	old_face = face_dir
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
		old_face = face_dir
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

	#coordinates of the pusedo nodes

	d12 = (d00+d1)/2 
	x12 = np.array([	f['x'](d12),
						f['y'](d12),
						f['z'](d12)])/1000
						
	#creates the rest of the psuedonode for this step
	step = int(step)
	psuedo = np.array([['up'],
					['down'],
					['left'],
					['right']])
	ste = [step]*4
	
	#gets coords of psuedo nodes
	t12 = average_angle(face_dir,old_face)
	R = np.transpose(rotZ(t12))

	p_nodes = pd.DataFrame.from_records(psuedo,columns = ['direction'])
	p_nodes['step'] = ste
	p_nodes['x'] = [0,0,-template['width']/2,template['width']/2]
	p_nodes['z'] = [template['width']/2,-template['width']/2,0,0]
	p_nodes['y'] = [0,0,0,0]
	p_nodes[['x','y','z']] = p_nodes[['x','y','z']].dot(R)
	p_nodes['x'] += x12[0]
	p_nodes['y'] += x12[1]
	p_nodes['z'] += x12[2]
	pseudo_nodes =  pseudo_nodes.append(p_nodes,ignore_index = True)
	return face_dir,nodes,elements,pseudo_nodes
