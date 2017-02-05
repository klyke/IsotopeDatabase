from isotopes import IsotopeDatabase, Isotope
import matplotlib.pyplot as plt
import numpy as np


def isotopes_of_interest(iso_db):
	#			H-1,    He-4,  Fe-56,    Ni-62,    U-235,     U-238
	nucleons = [(1,1), (2,4), (26, 56), (28, 62), (92, 235), (92, 238)]
	isos = [iso_db.getExactIsotope(*I) for I in nucleons]
	return isos

def main():
	DB = IsotopeDatabase("isotopes.txt")

	isos = sorted(DB.isotopes, key=lambda I: I.A)

	binding_energies = [I.getMassDefectBE()/I.A for I in isos]
	atomic_mass = [I.A for I in isos]

	features = isotopes_of_interest(DB)

	plt.figure()
	plt.plot(atomic_mass, binding_energies, label="Mass Defect")

	for I in features:
		x = I.A
		y = I.getMassDefectBE()/I.A
		plt.plot(x, y, 'o', color="red")
		plt.annotate(I.name+str(x), (x,y))

	plt.xlabel("Atomic Number")
	plt.ylabel("BE(MeV) / A")
	plt.legend(loc='best')
	plt.grid()
	plt.show()


if __name__ == '__main__':
    main()
