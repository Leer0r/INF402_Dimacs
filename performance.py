import datetime
import os
import subprocess


def affiche_result(start, stop):
    res = stop - start
    print("Performance du programme : {}".format(res))


args = os.sys.argv

if len(args) == 1:
    print("Veuillez entrez un fichier d'entrée")
    exit(1)

with open("data/{}.tak".format(args[1]), "r") as fichier:
    length = fichier.readline().replace("\n", "")

print("Test pour une grille de {}x{}".format(length, length))
print("\n_________________________________________________________________\nDébut du test de performance \n_________________________________________________________________\n")
start = datetime.datetime.now()
subprocess.run(["python3", "main.py", "{}".format(args[1])])
stop = datetime.datetime.now()
print("_________________________________________________________________\n Fin du test de performance\n_________________________________________________________________\n")
affiche_result(start, stop)
