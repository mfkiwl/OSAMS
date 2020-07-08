"""
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
**Viscoelastic, time=PRONY
** 0.01,  0., 0.1
** 0.35,  0.,  1.
** 0.24,  0.,  7.
**0.21,  1.,100.
**Trs
"""
def materiel_model():
	return ("""
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMAN=5.6703E-8
*Material, name=ABSP430
*Conductivity
0.3,
*Density
1040.,
*Elastic
2200e6., 0.4, 20
1100e6., 0.4, 100
*PLASTIC, HARDENING=ISOTROPIC
31e6, 0.0, 20
33e6, 0.05, 20
15.5e6, 0.0, 90
16.5e6, 0.05, 90
*Expansion
8.82e-05,
*Specific Heat
2020
""")

def section():
	return """*SOLID SECTION, ELSET=ALLELEMENTS, MATERIAL = ABSP430"""
