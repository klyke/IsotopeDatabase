import os
import sys


class Isotope(object):
    def __init__(self,name,  Z, A, M):
        self.name = name
        self.Z = Z
        self.A = A
        self.N = A-Z
        self.M = M

    def getMassDefectBE(self):
        mP = 938.272 #MeV/c2
        mN = 939.565 #MeV/c2
        u = 931.494 #Mev/c2

        return self.Z*mP + self.N*mN - self.M*u

    def getSemiEmpericalBE(self):
        aV = 15.8
        aS = 18.3
        aC = 0.714
        aA = 23.2
        aP = 0.0

        A = self.A
        N = self.N
        Z = self.Z

        if Z%2 == 0 and N%2 == 0:
            aP = 12.0
        elif Z%2 == 1 and N%2 == 1:
            aP = -12.0

        BE = aV*A - aS*(A**(2/3)) \
            - aC * ((Z**2)/(A**(1/3))) \
            - (aA/A) * ((A - 2*Z)**2) \
            + aP/(A**(1/2))

        return BE

class IsotopeDatabase(object):
    def __init__(self, path_to_database):
        if not os.path.exists(path_to_database):
            print("Invalid database path.")
            sys.exit()
        self.loadDatabase(path_to_database)

    def loadDatabase(self, db_path):
        isotopes = []
        currentZ = 0
        currentName = None
        with open(db_path, "r") as infile:
            for line in infile:
                if line.startswith("_") or line == "\n" or line[0].isalpha():
                    continue

                elif line[0].isdigit():
                    data = line.split()
                    currentZ = int(data[0])
                    currentName = data[1]
                    A = int(data[2])
                    i = data[3].index("(")
                    M = float(data[3][:i])
                    isotopes.append(Isotope(currentName, currentZ, A, M))

                else:
                    data = line.split()
                    A = int(data[0])
                    i = data[1].index("(")
                    M = float(data[1][:i])
                    isotopes.append(Isotope(currentName, currentZ, A, M))

        self.isotopes = isotopes

    def filterIsotopes(self, f):
        return [isotope for isotope in self.isotopes if f(isotope)]

    def getIsotopesByName(self, name):
        f = lambda I: I.name.upper() == name.upper()
        return self.filterIsotopes(f)

    def getIsotopesByZ(self, Z): 
        f = lambda I: I.Z == Z
        return self.filterIsotopes(f)

    def getIsotopesByN(self, N):
        f = lambda I: I.N == N
        return self.filterIsotopes(f)

    def getExactIsotope(self, Z, A):
        f = lambda I: I.A == A and I.A == A
        return self.filterIsotopes(f)[0]


