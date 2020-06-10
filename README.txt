NODES:
	NODE TYPES:
		BUILD_PLATE:	belongs to the build plate so zero displacement
		FREE_SURFACE:	nodes on the outside of the part 
		INTERIEOR:		nodes on interior voids
		MERGED:			nodes that experienced a MERGE operation and will be able to have interface strength predicted given temperature data throughout the step

SETS:
	NODE SETS:
		BUILD_PLATE:	nodes that are on the build plate (constant for all STEP)
	
	ELEMENT SETS:
		E_STEP_{N}:		elements that are deposited during STEP {N}
SURFACES:
	{N}_{DIRECTION}:	the {DIRECTION} surface extruded in STEP {N}

	
ELEMENTS
	elements are organized by the STEP they are are deposited in

STEPS:

all STEP correspond to a stepin the ABAQUS analysis

change STEP options by changing values in steps.CSV
OPTIONS:
	DT: 		The length of time the STEP occurs over
	BP_T:		The Build Plate Temperature at the start of the step
	SOL_T:		the solution technique for the step (SEPARATED or)
	enclosure:	The enclosure temperature
	h_nat:		the convection cooefficent for FREE surfaces
	fan:		convection cooeffcient for HOT surfaces = h_nat*(1+fan}





