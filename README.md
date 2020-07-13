# Open Source Additive Manufacturing Simulator (OSAMS)

(c) 2020 Christopher C. Bock


## About This Repository
- This is a python package that creates models of the additive manufacturing process
- The OSAMS folder contains the actual package, everything else is extras
- Currently this package generates .inp files for abaqus
- Currently the package is still new, so reverse compatibility between any two versions is not guaranteed

## Comments:
most functions are commented like so:

```
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
def my_funct(a,b)
	c = a+b		c: sum of a and b
	d = a-b
	return(c,d)
```
## TODO:
# Validation and Accuracy (HIGH):
- nozzle heat method
- build plate adhesion
# Housekeeping (LOW)
- comment all functions
- move helper functions
- add gcode glossary
- add user defined machine behaviour
- PyPi
- fix the issue where there are multiple empty steps at the beginning of the analysis
- give users the option to 
