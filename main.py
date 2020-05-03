# imports
import sys
import os

# constants
DATA_PATH = './data'
EXT_FILE = 'tak'
OUT_FILE = 'dimacs'
CHARS = ['0', '1', '_']

# argument number
argc = len(sys.argv) - 1

# must have the good number of argument
if argc != 1:
    print("Erreur, 1 argument requis : nom du fichier dans le répertoire data/")
    sys.exit(1)


# argv[0] = nom du fichier
# argv[1] = argument 1 : nom du fichier

def k_arrangement(n, k):
    if n == 0:
        yield []
    else:
        if k < n:
            for y in k_arrangement(n-1, k):
                yield y + [0]
        if k > 0:
            for y in k_arrangement(n-1, k-1):
                yield y + [1]



class ConvertisseurDIMACS:

    def __init__(self, file_path):
        self.size = 0
        tab = []
        # file not exists or is'nt a file
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            print("Erreur: le chemin doit amener vers un fichier existant", file_path)
            sys.exit(2)

        # read file
        with open(file_path, "r") as file:
            # check array size
            self.size = file.readline().replace('\n', '')

            # check valid arg
            if (not self.size.isdigit()) or (int(self.size) < 0):
                print("Erreur, la première ligne du fichier doit être un entier positif")
                sys.exit()

            # convert to integer
            self.size = int(self.size)

            # create array
            self.tab = []
            for i in range(self.size):
                line = file.readline().replace('\n', '')

                # line too small
                if len(line) < self.size:
                    print("Erreur de longueur de ligne à la ligne", i+2)
                    sys.exit()

                # line contains illegal character(s)
                if not all(x in CHARS for x in line):
                    print("Erreur: 0, 1 ou _ accepté")
                    sys.exit()

                # all's good
                self.tab.append(line[:self.size])

    def ecrireDIMACS(self, file_path):
        with open(file_path,"w") as f:

            #Rule 1
            self.eq_ligne(f)
            self.eq_colonne(f)

            #Rule 2
            self.sim_ligne(f)
            self.sim_colonne(f)

            #Rule 3
            self.unique_ligne(f)
            self.unique_colonne(f)

    # RULES:
    # 1 - need to have equal number of 0 and 1 on all rows / columns
    # 2 - no more than 2 same numbers in a raw
    # 3 - each row / column has to be unique   


    # doute de timon (on a fait des ou de et il faut faire de et de ou)
    def eq_ligne(self, f):
        for arrangement in k_arrangement(self.size, self.size//2) :
            for j in range(self.size):
                index = [i + j*self.size for i in range(self.size)]
                text = ""
                for n in range(self.size):
                    text += ('-' if arrangement[n] == 0 else '') + str(index[n]) + ' '
                f.write(text)
                f.write("\n")


    def eq_colonne(self, f):
        for arrangement in k_arrangement(self.size, self.size//2) :
            for i in range(self.size):
                index = [i + j*self.size for j in range(self.size)]
                text = ""
                for n in range(self.size):
                    text += ('-' if arrangement[n] == 0 else '') + str(index[n]) + ' '
                f.write(text)
                f.write("\n")

            

    def sim_ligne(self, f):
        for i in range(1, self.size - 1):
            for j in range(0, self.size):
                index = [(i-1) + j * self.size, i + j * self.size, (i+1) + j * self.size]
                f.write(str(index[0]) + " " + str(index[1]) + " " + str(index[2]))
                f.write(" -" + str(index[0]) + " -" + str(index[1]) + " -" + str(index[2]))
            f.write("\n")


    def sim_colonne(self, f):
        for i in range(0, self.size):
            for j in range(1, self.size - 1):
                index = [i + (j-1) * self.size, i + j * self.size, i + (j+1) * self.size]
                f.write(str(index[0]) + " " + str(index[1]) + " " + str(index[2]))
                f.write(" -" + str(index[0]) + " -" + str(index[1]) + " -" + str(index[2]))
            f.write("\n")

    def unique_ligne(self, f):
        pass

    def unique_colonne(self, f):
        pass



# execute

c = ConvertisseurDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], EXT_FILE))

c.ecrireDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], OUT_FILE))