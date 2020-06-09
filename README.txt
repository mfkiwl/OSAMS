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
		E_STEP_N:		elements that are deposited during STEP N
SURFACES:
	INTERIOR_N:	surfaces that become internal during STEP N
	BOND_N:		surfaces that become bond surfaces during STEP N
	HOT_N:		surfaces that become hot during step N and then external during step N+1	
	
ELEMENTS
	elements are organized by the STEP they are are deposited in

STEPS:

all STEP correspond to a stepin the ABAQUS analysis

change STEP options by changing values in steps.CSV
OPTIONS:
	DT: 	The length of time the STEP occurs over
	BP_T:	The Build Plate Temperature at the start of the step
	SOL_T:	the solution technique for the step (SEPARATED or)
	FAN:	(0-100) percent on of the fans of the extruder (UNIMPLEMENTED)





