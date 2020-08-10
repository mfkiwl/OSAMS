import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
angle between two vectors 
"""
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v2, v1):
	theta = np.arctan2(v2[1],v2[0])
	return theta

def clockwise(theta1,theta2):
	if (theta1 <= theta2):
		theta2 -= np.pi *2 
	arc = np.abs(theta1-theta2)
	return np.linspace(theta1,theta2),arc

def c_clockwise(theta1,theta2):
	if (theta1 >= theta2):
		theta2 += np.pi * 2
	arc = np.abs(theta1-theta2)
	return np.linspace(theta1,theta2),arc

def read_path(g_code):
	cmds = g_code.splitlines()
	
	#MACHINE STATE
	position = np.array([0.0,0.0,0.0])
	temperatures = [0.0] 
	times = [0.0] 
	fan_speeds = [0.0] 
	bed_temperatures = [0.0]
	distances = [0.0]
	enclosures = [20.0]
	layers = 0.0

	#PERSISTENT MACHINE STATE
	feed_speed = 0.0
	fan_speed = 0.0
	time = 0.0
	bed_temperature = 0.0
	temperature = 0.0
	total_distance = 0.0
	enclosure = 20.0
	layer = 0.0
	
	offset = np.array([0.0,0.0,0.0])


	#HOW TO USE THIS INTERPRITER
	#E0 - NON EXTRUSION
	#E1 - EXTRUSION

	path = np.array([position.copy()])
	extruding = [0]
	#INTERPRITER

	for i in cmds:
		words = i.split()
		#LINEAR MOVE
		if (words[0][0] == ";"):
			pass
		elif (words[0] == "G92"):
			for j in words[1:]:
				#READS DESTINATION LOCATION
				prefix = j[0]
				if (prefix == "X"):
					offset[0] = float(j[1:])
				if (prefix == "Y"):
					offset[1] = float(j[1:])
				if (prefix == "Z"):
					offset[2] = float(j[1:])

		elif (words[0] == "G1" or words[0] == "G0"):
			e = 0
			P1 = position.copy()

			#where does the head go
			for j in words[1:]:
				#READS DESTINATION LOCATION
				prefix = j[0]
				if (prefix == "X"):
					position[0] = float(j[1:])
				if (prefix == "Y"):
					position[1] = float(j[1:])
				if (prefix == "Z"):
					position[2] = float(j[1:])
				if (prefix == "F"):
					feed_speed = float(j[1:])/60
				if (prefix == "E"):
					e = int(int(j[1:])>0)

			extruding.append(e)

			
			position = position + offset 
			D = np.linalg.norm(position-P1)

			#UPDATES THE TIME
			time = time + D/feed_speed
			times.append(time)

			#UPDATES MACHINE STATE
			bed_temperatures.append(bed_temperature)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			total_distance += D
			distances.append(total_distance)
			enclosures.append(enclosure)

			path = np.append(path,position)
		
		#ARC - ANYTHING BEYOND G0-G3 IS AT LARGE
		#NOMINALLY IN I J FORM
		#IGNORES Z
		elif (words[0] == "G2" or words[0] == 'G3'):
			arc_inc = 50
			P1 = position
			P2 = position.copy()
			P3 = position.copy()
			for j in words[1:]:
				#READS DESTINATION LOCATION
				prefix = j[0]
				if (prefix == "X"):
					P3[0] = float(j[1:])
				elif (prefix == "Y"):
					P3[1] = float(j[1:])
				elif (prefix == "I"):
					P2[0] = P1[0] + float(j[1:])
				elif (prefix == "J"):
					P2[1] = P1[1] + float(j[1:])
			
			#angle between the two points
			X = np.array([1,0,0]) #UNIT VECTOR

			#finds the angles of the two points relative to the other things
			theta1 = angle_between(P1-P2,X)
			theta2 = angle_between(P3-P2,X)
			
			#clockwise or anticlockwise
			R = np.linalg.norm(P2-P1)
			if (words[0][1] == '2'):
				thetas,arc = clockwise(theta1,theta2)
			else:
				thetas,arc = c_clockwise(theta1,theta2)
			
			arc_dist = R * arc
			R1 = np.array([np.cos(thetas)*R+P2[0],np.sin(thetas)*R+P2[1],0*thetas+P2[2]])
			R1 = R1.transpose()

			arc_time = (arc_dist/feed_speed)

			#distance traveled with each arc increment
			D = np.abs(thetas - theta1)*R

			ex_times = (D/feed_speed) + time

			#UPDATES MACHINE STATES
			distances = distances + list(D+total_distance)
			total_distance += arc_dist
			distances.append(total_distance)

			#time
			times = times + list(ex_times)
			time += arc_time
			times.append(time)

			arc_inc = arc_inc + 1
			extruding = extruding + [1] * arc_inc 
			temperatures = temperatures + [temperature] * arc_inc
			enclosures = enclosures + [enclosure] * arc_inc
			bed_temperatures = bed_temperatures + [bed_temperature] * arc_inc
			fan_speeds = fan_speeds + [fan_speed] * arc_inc

			#moves tool head
			position = P3
			path = np.append(path,R1)
			path = np.append(path,P3)



		elif (words[0] == 'M104'):
			time += 1 
			temperature = float(words[1][1:])
			bed_temperatures.append(bed_temperature)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			path = np.append(path,position)
			times.append(time)
			distances.append(total_distance)
			enclosures.append(enclosure)
			extruding.append(0)
	
		elif (words[0] == 'M106'):
			fan_speed = float(words[1][1:])
			time += 1
			bed_temperatures.append(bed_temperature)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			path = np.append(path,position)
			times.append(time)
			distances.append(total_distance)
			enclosures.append(enclosure)
			extruding.append(0)

		elif (words[0] == 'M140'):
			time += 1
			bed_temperature = float(words[1][1:])
			bed_temperatures.append(bed_temperature)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			path = np.append(path,position)
			times.append(time)
			distances.append(total_distance)
			enclosures.append(enclosure)
			extruding.append(0)

		#DWELL
		elif (words[0] == 'G4'):
			if (words[1][0] == 'P'):
				time = time + float(words[1][1:])/1000

			elif (words[1][0] == 'S'):
				time = time + float(words[1][1:])


			#UPDATES MACHINE STATE
			extruding.append(0)
			bed_temperatures.append(bed_temperature)
			enclosures.append(enclosure)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			path = np.append(path,position)
			times.append(time)
			distances.append(total_distance)

		elif (words[0] == 'C2'):
			enclosure = float(words[1][1:])
			bed_temperatures.append(bed_temperature)
			enclosures.append(enclosure)
			temperatures.append(temperature)
			fan_speeds.append(fan_speed)
			path = np.append(path,position)
			times.append(time)
			distances.append(total_distance)
			
	
	pa = np.transpose(np.array([distances,times,temperatures,fan_speeds,bed_temperatures,extruding]))	
	path_states = pd.DataFrame(pa, columns = ['distance','time', 'temp','fan','b_temp','extruding'])
	path = path.reshape((-1,3))
	
	x = pd.DataFrame(path,columns = ['x','y','z'])

	path_states = path_states.join(x)
	return path_states
		
			
#CODE = """M104 T200
#M106 F100 
#M140 T60
#G1 X0 Y0 Z0 F80
#G1 X4 Y0 Z0
#G3 X4 Y2 I0 J1
#G1 X0 Y2 Z0
#G2 X0 Y4 I0 J1
#"""
#R1 = read_path(CODE)
#R1 = np.reshape(R1,(-1,3))
#R1 = R1.transpose()
#
#dx = np.gradient(R1[0,:])
#print(dx)
#dy = np.gradient(R1[1,:])
##plt.plot(dx)
##plt.plot(dy)
##plt.show()
#
			
			
