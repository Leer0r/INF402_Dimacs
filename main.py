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
        self.list_possible = [dec2bin(i, self.size)
                              for i in range((2**self.size))]  # Liste de toute les possibilitée pour pouvoir déterminé celle qui ne respècte pas les deux premières règles

    def ecrireDIMACS(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            compt_line: int = 1
            f.write("p cnf {} {}\n".format(self.size**2, 0))
            for i in range(len(self.tab)):
                for j in range(len(self.tab)):
                    if self.tab[i][j] == "0":
                        f.write("-{}\n".format(self.index(j+1, i)))
                        compt_line += 1
                    elif self.tab[i][j] == "1":
                        f.write("{}\n".format(self.index(j+1, i)))
                        compt_line += 1

            list_exclue: list = []
            for i in self.list_possible:
                if not self.verif_ligne_col(i) or self.verif_suite(i):
                    list_exclue.append(i)
            tab_tmp: list = []
            for i in range(0, self.size**2, self.size):
                tab_tmp.append([j for j in range(i, i+self.size)])
            tab_ligne: list = []
            tab_colonne: list = []
            for i in range(0, self.size):
                tab_ligne.append([str(j)
                                  for j in range(i*self.size, (i+1)*self.size)])
                tab_colonne.append([str(j)
                                    for j in range(i, self.size**2, self.size)])
            for a in list_exclue:
                for b in tab_ligne:
                    for n in range(self.size):
                        if a[n] == "1":
                            f.write("-")
                        f.write(str(int(b[n]) + 1) + " ")
                    f.write("0\n")
                    compt_line += 1
                for b in tab_colonne:
                    for n in range(self.size):
                        if a[n] == "1":
                            f.write("-")
                        f.write(str(int(b[n]) + 1) + " ")
                    f.write("0\n")
                    compt_line += 1

            for a in self.list_possible:
                for n in range(len(tab_ligne)):
                    for m in range(n+1, len(tab_ligne)):
                        for i in range(self.size):
                            if a[j] == "0":
                                f.write(
                                    "-{} ".format(str(int(tab_ligne[n][i])+1)))
                                f.write(
                                    "-{} ".format(str(int(tab_ligne[m][i])+1)))
                            else:
                                f.write("{} ".format(
                                    str(int(tab_ligne[n][i])+1)))
                                f.write("{} ".format(
                                    str(int(tab_ligne[m][i])+1)))
                        f.write("0\n")
                        compt_line += 1

                for n in range(len(tab_colonne)):
                    for m in range(n+1, len(tab_colonne)):
                        for i in range(self.size):
                            if a[j] == "0":
                                f.write(
                                    "-{} ".format(str(int(tab_colonne[n][i])+1)))
                                f.write(
                                    "-{} ".format(str(int(tab_colonne[m][i])+1)))
                            else:
                                f.write("{} ".format(
                                    str(int(tab_colonne[n][i])+1)))
                                f.write("{} ".format(
                                    str(int(tab_colonne[m][i])+1)))
                        f.write("0\n")
                        compt_line += 1

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

    # ---- 1D ARRAY FORMAT ------
    #
    # retourne une ligne du tableau 2D grâce à un index sur un tableau 1D

    def row(self, i: int) -> list:
        return [self.tab[k] for k in range(i*self.size, i*self.size + self.size)]

    # retourne une colonne du tableau 2D grâce à un index sur un tableau 1D
    def col(self, i: int) -> list:
        return [self.tab[k*self.size + i] for k in range(self.size)]

    # retourne l'index 1D d'un élément depuis un index 2D
    def index(self, i: int, j: int) -> int:
        return i + j * self.size
    #
    # -----------------------------


# execute
c = ConvertisseurDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], EXT_FILE))
c.ecrireDIMACS("{}/{}.{}".format(DATA_PATH, sys.argv[1], OUT_FILE))
