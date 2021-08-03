import os


def Sauvegarde(score):
    chemin = os.getcwd()
    if not os.path.isdir(chemin + "\\Sauvegardes"):
        os.makedirs(chemin + "\\Sauvegardes")
        fich = open("Sauvegardes\\data_sond.txt", "w", encoding="utf8")
        fich.write("{:^4d}".format(0))
    fich = open("Sauvegardes\\data_sond.txt", "r", encoding="utf8")
    scoremax = (fich.readline())
    scoremax = int(scoremax)
    if score > scoremax:
        fich = open("Sauvegardes\\data_sond.txt", "w", encoding="utf8")
        fich.write("{:^4d}".format(score))
        scoremax = score

    fich.close()
    return scoremax
