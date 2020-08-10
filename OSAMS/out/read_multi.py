import shutil
import os

def read_multi(t_file,tag):
	'''
	reads multiple lines from a file 
	start of read area denoted by @TAG
	end by @END_{TAG}
	args:
		t_file: file
		tag: tag
	'''
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	read_line = ""
	reading = False
	for sline in old:
		line = sline.strip()
		if line==(f"@{tag}"):
			reading = True
		if (reading == False):
			new.write(sline)
		if (line==(f"@END_{tag}")):
			reading = False
		if (reading == True):
			read_line = read_line + sline
	old.close()
	new.close()
	os.remove(t_file+'~')
	return read_line

