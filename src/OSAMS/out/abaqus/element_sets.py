"""
CREATES THE ELEMENT SET DEFINITIONS FOR THE INP FILE
ARGS:
	ELEMENTS:	dataframe of elements
	step_nums:	the step indices to have sets made
"""
def element_sets(elements,steps):
	esets = "**ELEMENTS BY DEPOSISTION STEP"
	for i,row in steps.iterrows():
		if (row['type'] == 1):
			#SELECTS ELEMENTS DEPOSITED FOR THAT STEP
			step_elements = elements.loc[elements['step'] == i]
			#print(step_elements)
			#print("*********************************")

			#HEADER AND FIRST ELEMENT
			es_def = f"\n*ELSET, ELSET = E_STEP_{i}"
			es_def = es_def + f"\n{step_elements.index[0] + 1}"

			for i,row in step_elements[1:].iterrows():
				es_def = es_def + f",\n{i+1}"

			esets = esets + es_def
	#END
	esets = esets + '\n'
	return esets
