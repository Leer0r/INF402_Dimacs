# imports
import sys
import os
import copy
# constants
DATA_PATH = './data'
EXT_FILE = 'tak'
OUT_FILE = 'cnf'
CHARS = ['0', '1', '_']

# argument number
argc = len(sys.argv) - 1

# must have the good number of argument
if argc != 1:
    print("Erreur, 1 argument requis : nom du fichier dans le répertoire data/")
    sys.exit(1)


# argv[0] = nom du programme
# argv[1] = argument 1 : nom du fichier dans le dossier data/ sans l'extension .tak
# exemple: python main.py 1
#   donne l'execution du fichier data/1.tak

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


def dec2bin(d, nb=8):
    """Représentation d'un nombre entier en chaine binaire (nb: nombre de bits du mot)"""
    if d == 0:
        return "0".zfill(nb)

    if d < 0:
        d += 1 << nb

    b = ""

    while d != 0:
        d, r = divmod(d, 2)
        b = "01"[r] + b

    return b.zfill(nb)



class ConvertisseurDIMACS:

    def __init__(self, file_path):
        self.size = 0
        self.tab = []
        self.compteur_ligne = 0

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

        self.liste_possibles = [dec2bin(i, self.size) for i in range((2**self.size))]  # Liste de toute les possibilitée pour pouvoir déterminé celle qui ne respècte pas les deux premières règles

    def ecrireDIMACS(self, file_path: str) -> None:
        self.compteur_ligne: int = 1
        self.content = ''

        with open(file_path, "w") as f:
            #self.write("p cnf {} {}\n".format(self.size**2, 0))

            for i in range(len(self.tab)):
                for j in range(len(self.tab)):
                    
                    if self.tab[i][j] == "0":
                        self.write("-{}\n".format(self.index(j+1, i)))

                    elif self.tab[i][j] == "1":
                        self.write("{}\n".format(self.index(j+1, i)))

            liste_exclus: list = []

            for i in self.liste_possibles:
                if not self.verif_ligne_col(i) or self.verif_suite(i):
                    liste_exclus.append(i)

            tab_tmp: list = []

            for i in range(0, self.size**2, self.size):
                tab_tmp.append([j for j in range(i, i+self.size)])

            tab_ligne: list = []
            tab_colonne: list = []

            for i in range(0, self.size):
                tab_ligne.append([str(j) for j in range(i*self.size, (i+1)*self.size)])
                tab_colonne.append([str(j) for j in range(i, self.size**2, self.size)])
                
            for a in liste_exclus:
                for b in tab_ligne:
                    for n in range(self.size):
                        if a[n] == "1":
                            self.write("-")

                        self.write(str(int(b[n]) + 1) + " ")

                    self.write("0\n")

                for b in tab_colonne:
                    for n in range(self.size):
                        if a[n] == "1":
                            self.write("-")

                        self.write(str(int(b[n]) + 1) + " ")

                    self.write("0\n")

            for a in self.liste_possibles:
                for n in range(len(tab_ligne)):
                    for m in range(n+1, len(tab_ligne)):
                        for i in range(self.size):
                            if a[j] == "0":
                                self.write("-{} ".format(incrVal(tab_ligne[n][i])))
                                self.write("-{} ".format(incrVal(tab_ligne[m][i])))
                            else:
                                self.write("{} ".format(incrVal(tab_ligne[n][i])))
                                self.write("{} ".format(incrVal(tab_ligne[m][i])))
                                    
                        self.write("0\n")

                for n in range(len(tab_colonne)):
                    for m in range(n+1, len(tab_colonne)):
                        for i in range(self.size):
                            if a[j] == "0":
                                self.write("-{} ".format(incrVal(tab_colonne[n][i])))
                                self.write("-{} ".format(incrVal(tab_colonne[m][i])))
                            else:
                                self.write("{} ".format(incrVal(tab_colonne[n][i])))
                                self.write("{} ".format(incrVal(tab_colonne[m][i])))

                        self.write("0\n")

            self.content = "p cnf {} {}\n".format(self.size**2, self.compteur_ligne) + self.content
            f.write(self.content)
            f.close()


    def verif_ligne_col(self, tab: str):
        Z_count: int = 0
        O_count: int = 0

        for i in tab:
            if i == '0':
                Z_count += 1
            else:
                O_count += 1

        return Z_count == O_count

    def verif_suite(self, tab: str):
        for i in range(len(tab)-2):
            if tab[i] == tab[i+1] and tab[i+1] == tab[i+2]:
                return True
        return False

    # retourne l'index 1D d'un élément depuis un index 2D
    def index(self, i: int, j: int) -> int:
        return i + j * self.size

    # écrit dans le fichier f en rajoutant 1 au compteur de ligne. A n'utiliser que si \n dans content
    def write(self, content) -> None:
        self.content += content
        self.compteur_ligne += len(content.split('\n'))-1


def incrVal(val: str) -> int:
    return str(int(val)+1)
    


# execute
c = ConvertisseurDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], EXT_FILE))
c.ecrireDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], OUT_FILE))
