import pandas as pd


def materiel_model():
	return ("""
*Material, name=ABSP400
*Conductivity
 0.3,
*Density
1050.,
*Elastic, moduli=LONG TERM
2340e6., 0.4
*Expansion
 1e-05,
*Specific Heat
2020.,
*Viscoelastic, time=PRONY
 0.01,  0., 0.1
 0.35,  0.,  1.
 0.24,  0.,  7.
 0.21,  0.,100.
*Trs
108.,  8.86, 101.6""")

def section():
	return """
*SOLID SECTION, ELSET=ALLELEMENTS, MATERIAL = ABSP400"""
