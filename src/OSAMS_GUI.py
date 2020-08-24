'''
OSAMS_GUI
this is the code for the GUI interface
CHANGES
DATE		AUTHOR		CHANGE
2020.08.24	Chris Bock	Fixed Imported Modules
2020.8.24	Chris Bock	Tested
'''
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox
from run_funct import *
root = Tk()
root.title("OSAMS 0.99.1 GUI")

in_file = tkinter.StringVar()
in_file.set('N/A')
g_code = tkinter.StringVar()
g_code.set('N/A')
out_directory = tkinter.StringVar()
out_directory.set('N/A')
temp_file = tkinter.StringVar()
temp_file.set('N/A')
job_name = tkinter.StringVar()
job_name.set('N/A')

def get_path(f):
	the_file = tkinter.filedialog.askopenfilename(
	parent = root, title='choose file',
	filetypes=[f,('all files','.*')]
	)
	return the_file

	
def get_dir():
	the_file = tkinter.filedialog.askdirectory()
	return the_file

def run():
	job = job_name.get()
	template_file = temp_file.get()
	gc_file = g_code.get()
	inp_file = in_file.get()
	out_dir = out_directory.get()
	messagebox.showinfo('HELP')
	out_str = OSAMS_RUN(inp_file,out_dir,job,g_file=gc_file,template_path=template_file)
	#message_box(out_str)



mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='NESW')

ttk.Label(mainframe, text=f"Input File").grid(column=1, row=1, sticky=E)
ttk.Entry(mainframe, textvariable=f"{in_file}",width =  60).grid(column=2, row=1, sticky='NESW')
ttk.Button(mainframe, text='Browse', command = lambda:(in_file.set(get_path(('input files','.inp'))))).grid(column=3,row=1, sticky='NESW')

ttk.Label(mainframe, text="G Code").grid(column=1, row=2, sticky=E)
ttk.Entry(mainframe, textvariable=f"{g_code}",width =  60).grid(column=2, row=2, sticky='NESW')
ttk.Button(mainframe, text='Browse', command = lambda:(g_code.set( get_path(('g code','.GCODE'))))).grid(column=3,row=2, sticky=E)

ttk.Label(mainframe, text="Template").grid(column=1, row=3, sticky=E)
ttk.Entry(mainframe, textvariable=f"{temp_file}",width =  60).grid(column=2, row=3, sticky='NESW')
ttk.Button(mainframe, text='Browse', command = lambda:(temp_file.set(get_path(('Excel Workbook','.xlsx'))))).grid(column=3,row=3, sticky=E)

ttk.Label(mainframe, text="Job Name").grid(column=1, row=4, sticky=E)
#ttk.Label(mainframe, textvariable=f"{job_name}").grid(column=2, row=4, stickuuy=E)
ttk.Entry(mainframe, textvariable=job_name).grid(column=2,row=4,columnspan = 2,sticky='NESW')

ttk.Label(mainframe, text="Out Directory").grid(column=1, row=5, sticky=E)
ttk.Entry(mainframe, textvariable=f"{out_directory}",width =  60).grid(column=2, row=5, sticky='NESW')
ttk.Button(mainframe, text='Browse', command = lambda:(out_directory.set(get_dir()))).grid(column=3,row=5, sticky=E)

ttk.Button(mainframe, text='RUN',command=lambda: run()).grid(column=3,sticky=E)
ttk.Button(mainframe, text='About').grid(row= 6, column=1, sticky=W)

'''
ttk.Label(mainframe, text=f"Input File").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Thermal File").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Structural File").grid(column=1, row=3, sticky=W)
'''

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


root.mainloop()
