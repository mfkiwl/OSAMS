# Open Source Additive Manufacturing Simulator (OSAMS)

(c) 2020 Christopher C. Bock


## About This Repository
- This is a python package that creates models of the additive manufacturing process
- The src folder contains all of the source code
- The example folder contains example g code .inp files 
- The doc folder contains documentation for the package
- Currently this package generates .inp files for abaqus
- Currently the package is still new, so reverse compatibility between any two versions is not guaranteed

## Comments:
Most files are commented like so:
```
"""
file_name.py
this file contains code for the sum and difference of two numbers
CHANGES
DATE		AUTHOR		CHANGE
YYYY.MM.DD	Chris Bock	Fixed bug where difference was being saved to e
"""
def my_funct(a,b)
	"""
	my_funct
	this returns the sum and difference of two numbers
	args:
		a:	first number
		b:	second number
	returns:
		c:	sum of the numbers
		d:	difference of the numbers
	"""
	c = a+b		#c: sum of a and b
	#e = a-b
	d = a-b
	return(c,d)
```
## TODO:
- Validate warpage estimates
