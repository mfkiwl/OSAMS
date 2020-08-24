import shutil
import os

def ins_tag(t_file,tag,text):
	'''
	ins_tag
	inserts {text} to a tag in a file
	args;
		t_file: file
		tag: tag to insert at
		text: text to insert
	'''
	shutil.move(t_file,t_file+"~")
	old = open(t_file+"~",'r')
	new = open(t_file,'w')
	for sline in old:
		line = sline.strip()
		if line==(f"@{tag}"):
			new.write(text) 
		else:
			new.write(sline)
	old.close()
	new.close()
	os.remove(t_file+'~')

