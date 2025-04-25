#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:51:52 2022

@author: druet
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:32:50 2022

@author: druet
"""
import random
import time


################### le message de bienvenue et d'explication ##################

def welcome_message():
    print("""
----------------------------------------------------------------------------
                        RÃ¨gles du jeu de Nim
----------------------------------------------------------------------------
RÃ¨gles : 1 - L'ordinateur joue contre lui-mÃªme.
         2 - Il utilise les mÃªmes probabilitÃ©s (la mÃªme machine) pour les deux joueurs.
         3 - Seulement 1 ou 2 bÃ¢tons peuvent Ãªtre retirÃ©s Ã  chaque coup.
         4 - Celui qui tire le dernier bÃ¢ton a gagnÃ©.

----------------------------------------------------------------------------
                           Apprentissage
----------------------------------------------------------------------------
L'ordinateur reÃ§oit une rÃ©compense pour les coups jouÃ©s par le cÃ´tÃ©
de la machine qui a gagnÃ© et une punition  pour les coups jouÃ©s par le cÃ´tÃ©
de la machine qui a perdu
----------------------------------------------------------------------------
""")

#### Nous faisons commencer l'ordinateur parce que le premier joueur a une
#### stratÃ©gie gagnante. Si le joueur commence et qu'il joue bien, la machine
#### perdra quoiqu'elle fasse et n'apprendra rien.

###############################################################################


################## dÃ©finition et impression de la position de jeu #############

def printboard(n):
    board=[]
    for _ in range(n):
        board.append("/")
    print("\n----------------------------------------------------------------------------")
    print("      ",*board, sep="   ")
    print("----------------------------------------------------------------------------\n")
    print("Il reste " + str(n) + " allumettes.")

###############################################################################

################ calcul de la probabilitÃ© de gain du joueur 1 (machine) #######
################ contre le joueur 2 (machine) #################################

def proba_gain(boulesjaunes,boulesrouges):
    probagain=0
    j=[0,0,0,0,0,0,0,0]
    r=[0,0,0,0,0,0,0,0]
    table_proba=[0,0,0,0,0,0,0,0]
    for i in range(8):
        j[i]=boulesjaunes[i]/(boulesjaunes[i]+boulesrouges[i])
        r[i]=boulesrouges[i]/(boulesjaunes[i]+boulesrouges[i])
    table_proba[0]=1 ### s'il reste 1 allumette, le joueur gagne
    table_proba[1]=r[1] ### s'il reste 2 allumettes, le joueur gagne s'il joue rouge
    table_proba[2]=j[2]*j[1]
    table_proba[3]=r[3]*j[1]+j[3]*r[2]+j[3]*j[2]*r[1]
    table_proba[4]=r[4]*r[2]*table_proba[0]+(r[4]*j[2]+j[4]*r[3])*table_proba[1]+j[4]*j[3]*table_proba[2]
    table_proba[5]=r[5]*r[3]*table_proba[1]+(r[5]*j[3]+j[5]*r[4])*table_proba[2]+j[5]*j[4]*table_proba[3]
    table_proba[6]=r[6]*r[4]*table_proba[2]+(r[6]*j[4]+j[6]*r[5])*table_proba[3]+j[6]*j[5]*table_proba[4]
    table_proba[7]=r[7]*r[5]*table_proba[3]+(r[7]*j[5]+j[7]*r[6])*table_proba[4]+j[7]*j[6]*table_proba[5]
    return table_proba[7]

###############################################################################



################### initialisation de la machine ##############################

nombre_allumettes=8 ### vous pouvez changer le nombre d'allumettes de dÃ©part
board = [] ### le plateau de jeu
boulesjaunes = [] ### correspond au nombre de boules jaunes dans la case
boulesrouges = [] ### correspond au nombre de boules rouges dans la case
tirage = [] ### correspondra au tirage dans une partie
for _ in range(nombre_allumettes):
    boulesjaunes.append(2)
    boulesrouges.append(2)
    tirage.append(0)
#### Attention Python commence Ã  0 #####
boulesrouges[0]=0 #### il ne faut pas mettre de boules rouges dans la case 0, coup interdit


###############################################################################

#################### programme principal : jeu + renforcement #################
welcome_message()
uneautrepartie=True
compteur_partie=0
time.sleep(1)
pourcentage_gain=round(100*proba_gain(boulesjaunes,boulesrouges),2)
print("La probabilitÃ© de gain du joueur 1 Ã  la premiÃ¨re partie est de " + str(pourcentage_gain) +" %")
time.sleep(1)

while uneautrepartie :
    player = "CMP1"
    allumettes=nombre_allumettes
    tirage_1=[0,0,0,0,0,0,0,0]
    tirage_2=[0,0,0,0,0,0,0,0]
    while allumettes>0:
        printboard(allumettes)  ### imprime la position de jeu
        time.sleep(1)
        if player=='CMP1': ### c'est au joueur 1 de jouer
            print("\nL'ordinateur-joueur 1 choisit de retirer...")
            time.sleep(1)
            somme=boulesjaunes[allumettes-1]+boulesrouges[allumettes-1]
            boulehasard=random.randint(1,somme)##permet de tirer jaune ou rouge
            if boulehasard <= boulesjaunes[allumettes-1]: ##la machine a tirÃ© jaune, i.e. elle enlÃ¨ve une allumette
                tirage_1[allumettes-1]=1
                allumettes=allumettes-1
                print("1 allumette.")
            else:
                tirage_1[allumettes-1]=2
                allumettes=allumettes-2
                print("2 allumettes.")
            if allumettes==0:
                winner='CMP1'
            else:
                player='CMP2'
        else: ### c'est au joueur 2 de jouer
            print("\nL'ordinateur-joueur 2 choisit de retirer...")
            time.sleep(1)
            somme=boulesjaunes[allumettes-1]+boulesrouges[allumettes-1]
            boulehasard=random.randint(1,somme)##permet de tirer jaune ou rouge
            if boulehasard <= boulesjaunes[allumettes-1]: ##la machine a tirÃ© jaune, i.e. elle enlÃ¨ve une allumette
                tirage_2[allumettes-1]=1
                allumettes=allumettes-1
                print("1 allumette.")
            else:
                tirage_2[allumettes-1]=2
                allumettes=allumettes-2
                print("2 allumettes.")
            if allumettes==0:
                winner='CMP2'
            else:
                player='CMP1'
    compteur_partie+=1
##### fin de la partie ######
##### annonce des rÃ©sultats #####
    if winner=='CMP1':
        print("\n----------------------------------------------------------------------------")
        print("Le joueur 1 a gagnÃ©. Nous allons maintenant rÃ©compenser les coups du joueur 1 et punir les coups du joueur 2.")
        print("----------------------------------------------------------------------------\n")
    else:
        print("\n----------------------------------------------------------------------------")
        print("Le joueur 2 a gagnÃ©. Nous allons maintenant rÃ©compenser les coups du joueur 2 et punir les coups du joueur 1.")
        print("----------------------------------------------------------------------------\n")
##### Apprentissage : rÃ©compense ou punition de l'ordinateur#####
    if winner=='CMP1': ###rÃ©compense du joueur 1 et punition du joueur 2
        for i in range(nombre_allumettes):
            if tirage_1[i]==1:
                boulesjaunes[i]=boulesjaunes[i]+1
            if tirage_1[i]==2:
                boulesrouges[i]=boulesrouges[i]+1
            if tirage_2[i]==1:
                boulesjaunes[i]=boulesjaunes[i]-1
            if tirage_2[i]==2:
                boulesrouges[i]=boulesrouges[i]-1
    else: ###rÃ©compense du joueur 2 et punition du joueur 1
        for i in range(nombre_allumettes):
            if tirage_2[i]==1:
                boulesjaunes[i]=boulesjaunes[i]+1
            if tirage_2[i]==2:
                boulesrouges[i]=boulesrouges[i]+1
            if tirage_1[i]==1:
                boulesjaunes[i]=boulesjaunes[i]-1
            if tirage_1[i]==2:
                boulesrouges[i]=boulesrouges[i]-1
####### fin de la rÃ©compense ou de la punition #################

####### fin de la rÃ©compense ou de la punition #################
####### rÃ©initialisation des verres vides ######################
    for i in range(nombre_allumettes):
        if (boulesjaunes[i]==0) and (boulesrouges[i]==0):
            boulesjaunes[i]=2
            boulesrouges[i]=2
######## impression de l'Ã©tat des verres #######################
    time.sleep(1)
    for i in range(nombre_allumettes):
        print("Dans le verre " + str(i+1) +", il y a " + str(boulesjaunes[i]) + " boules jaunes et " + str(boulesrouges[i]) + " boules rouges.")
################################################################
############ calcul de la probabilitÃ© de gagner ################
    time.sleep(1)
    pourcentage_gain = round(100*proba_gain(boulesjaunes,boulesrouges),2)
    print("\n----------------------------------------------------------------------------")
    print("L'ordinateur a jouÃ© "+ str(compteur_partie) +" parties.")
    print("----------------------------------------------------------------------------\n")
    print("\n----------------------------------------------------------------------------")
    print("La probabilitÃ© de gain du joueur 1 est de " + str(pourcentage_gain) +" %")
    print("----------------------------------------------------------------------------\n")

############ on continue ? #################
    test=True
    while test:
        another_go = input("\nVoulez-vous que l'ordinateur rejoue ? [O/N]: ")
        if another_go in ("o","O"):
            uneautrepartie=True
            test=False
        elif another_go in ("n","N"):
            uneautrepartie=False
            test=False
        else:
            print("\nChoix invalide. Recommencez !")
############################################