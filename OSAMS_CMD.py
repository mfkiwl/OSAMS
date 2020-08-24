import sys
import argparse
from run_funct import *

def main():
	p = argparse.ArgumentParser()
	p.add_argument('input',help='the .inp file')
	p.add_argument('job',help='the job name')
	p.add_argument('-g','--gcode',default='N/A',help='g code file, if omitted assumed to be provided in input file')
	p.add_argument('-t','--template',default='N/A',help='mesh template, if ommited assumed to be provided in input file')
	p.add_argument('-o','--output_directory',default='N/A', help='directory to place finished .inp files, if ommited will be placed in current directory')
	args = p.parse_args()
	#print(args.output_directory)
	#input('hfjkdhfdjklhafj')
	print(OSAMS_RUN(args.input,args.output_directory,args.job,g_file=args.gcode,template_path=args.template))

	
	

if __name__ == "__main__":
   main()
