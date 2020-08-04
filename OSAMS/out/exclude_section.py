import shutil
import os

def exclude_section(t_file,tag):
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	excluding = False
	for sline in old:
		line = sline.strip()
		if line==(f"**@{tag}"):
			excluding = True
			print("START")
		if (excluding == False):
			new.write(sline)
		if (line==(f"**@END_{tag}")):
			excluding = False
			print("FIN")
	old.close()
	new.close()
	os.remove(t_file+'~')

