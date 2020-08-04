import shutil
import os

def read_multi(t_file,tag):
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	read_line = ""
	reading = False
	for sline in old:
		line = sline.strip()
		if line==(f"**@{tag}"):
			reading = True
		if (reading == False):
			new.write(sline)
		if (line==(f"**@END_{tag}")):
			reading = False
		if (reading == True):
			readline += sline
	old.close()
	new.close()
	os.remove(t_file+'~')
	return read_line

