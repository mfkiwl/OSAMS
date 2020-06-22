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
- add support for C3
- comment all functions
- move helper functions
- add support for C1 - C3
- add gcode glossary
- add user defined machine behaviour
- improve handling of mesh templates
- PyPi
- improve node merging algorithim
- add support for sequentially coupled analysis
