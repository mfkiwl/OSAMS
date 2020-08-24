import shutil
import os

def read_string(t_file,tag):
	'''
	read_string
	reads a string denoted by @STRING@{TAG}="TEXT"
	args:
		t_file: file
		tag: tag
	'''
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	value = 0.0
	for sline in old:
		line = sline.strip()
		words = line.split('=')
		if words[0]==(f"@STRING@{tag}"):
			value = str(words[1])
			value = value.strip('\"')
		else:
			new.write(sline)
			pass
	old.close()
	new.close()
	os.remove(t_file+'~')
	return value
