import shutil
import os
def exclude_section(t_file,tag):
	'''
	exclude_section
	removes a section denoted by tags from a file
	args:
		t_file: file 
		tag: tag to remove
	the start of exvluded sections is denoted by @{TAG}
	the end of excluded sections is denoted by @END_{TAG}
	'''
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	excluding = False
	for sline in old:
		line = sline.strip()
		if line==(f"@{tag}"):
			excluding = True
			#print("START")
		if (excluding == False):
			new.write(sline)
		if (line==(f"@END_{tag}")):
			excluding = False
			#print("FIN")
	old.close()
	new.close()
	os.remove(t_file+'~')

