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
RÃ¨gles : 1 - L'utilisateur et l'ordinateur jouent Ã  tour de rÃ´le.
         2 - L'ordinateur commence.
         3 - Seulement 1 ou 2 bÃ¢tons peuvent Ãªtre retirÃ©s Ã  chaque coup.
         4 - Celui qui tire le dernier bÃ¢ton a gagnÃ©.

----------------------------------------------------------------------------
                           Apprentissage
----------------------------------------------------------------------------
Suivant qu'il gagne ou perd, l'ordinateur reÃ§oit une rÃ©compense ou une punition.
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
print("La probabilitÃ© de gain de l'ordinateur Ã  la premiÃ¨re partie si le joueur joue optimalement est de 12,5 %")
time.sleep(1)
while uneautrepartie :
    player = "CMP"
    allumettes=nombre_allumettes
    tirage=[0,0,0,0,0,0,0,0]
    while allumettes>0:
        printboard(allumettes)  ### imprime la position de jeu
        time.sleep(1)
        if player=='CMP': ### c'est Ã  l'ordinateur de jouer
            print("\nL'ordinateur choisit de retirer...")
            time.sleep(1)
            somme=boulesjaunes[allumettes-1]+boulesrouges[allumettes-1]
            boulehasard=random.randint(1,somme)##permet de tirer jaune ou rouge
            if boulehasard <= boulesjaunes[allumettes-1]: ##la machine a tirÃ© jaune, i.e. elle enlÃ¨ve une allumette
                tirage[allumettes-1]=1
                allumettes=allumettes-1
                print("1 allumette.")
            else:
                tirage[allumettes-1]=2
                allumettes=allumettes-2
                print("2 allumettes.")
            if allumettes==0:
                winner='CMP'
            else:
                player='USER'
        else: ### c'est au joueur de jouer
#### on demande au joueur ce qu'il souhaite jouer avec vÃ©rification que c'est un coup lÃ©gal
            coup_joueur=0
            print("\n--Ã€ vous de jouer !--")
            while coup_joueur not in range(1, 3) or coup_joueur>allumettes:
                try:
                    coup_joueur = int(input("\nQuel est votre choix ?"))
                    if coup_joueur == 0:
                        print("\nVous devez enlever au moins une allumette !")
                    elif coup_joueur not in range(1, 3) or coup_joueur>allumettes:
                        print("\nVous ne pouvez pas enlever autant d'allumettes !")
                        coup_joueur = int(input("\nQuel est votre choix ?"))
                except Exception as e:
                    print("\nCela ne semble pas une rÃ©ponse valide.\nError: " + str(e) + "\nRecommencez !")
##### fin du choix du joueur
            allumettes=allumettes-coup_joueur
            if allumettes==0:
                winner='USER'
            else:
                player='CMP'
    compteur_partie+=1
##### fin de la partie ######
##### annonce des rÃ©sultats #####
    if winner=='CMP':
        print("\n----------------------------------------------------------------------------")
        print("L'ordinateur a gagnÃ©, nous allons le rÃ©compenser.")
        print("----------------------------------------------------------------------------\n")
    else:
        print("\n----------------------------------------------------------------------------")
        print("Bravo ! Vous avez gagnÃ© ! Nous allons punir l'ordinateur.")
        print("----------------------------------------------------------------------------\n")
##### Apprentissage : rÃ©compense ou punition de l'ordinateur#####
    if winner=='CMP': ###rÃ©compense
        for i in range(nombre_allumettes):
            if tirage[i]==1:
                boulesjaunes[i]=boulesjaunes[i]+1
            if tirage[i]==2:
                boulesrouges[i]=boulesrouges[i]+1
    else: ###punition
        for i in range(nombre_allumettes):
            if tirage[i]==1:
                boulesjaunes[i]=boulesjaunes[i]-1
            if tirage[i]==2:
                boulesrouges[i]=boulesrouges[i]-1
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
    if (boulesjaunes[3]/(boulesjaunes[3]+boulesrouges[3]))>(boulesrouges[4]/(boulesjaunes[4]+boulesrouges[4])):
        proba=(boulesrouges[7]/(boulesjaunes[7]+boulesrouges[7]))*(boulesrouges[4]/(boulesjaunes[4]+boulesrouges[4]))*(boulesrouges[1]/(boulesjaunes[1]+boulesrouges[1]))
    else:
        proba=(boulesrouges[7]/(boulesjaunes[7]+boulesrouges[7]))*(boulesjaunes[3]/(boulesjaunes[3]+boulesrouges[3]))*(boulesrouges[1]/(boulesjaunes[1]+boulesrouges[1]))
    print("\n----------------------------------------------------------------------------")
    print("Vous avez jouÃ© "+ str(compteur_partie) +" parties.")
    print("----------------------------------------------------------------------------\n")
    print("\n----------------------------------------------------------------------------")
    print("La probabilitÃ© de gain de l'ordinateur Ã  la prochaine partie si le joueur joue optimalement (en connaissant l'Ã©tat des verres :-)) est de " + str(round(proba*100,2)) + "%")
    print("----------------------------------------------------------------------------\n")
################################################################
############ On continue ? ################
    test=True
    while test:
        another_go = input("\nVoulez-vous rejouer ?[O/N]: ")
        if another_go in ("o","O"):
            uneautrepartie=True
            test=False
        elif another_go in ("n","N"):
            uneautrepartie=False
            test=False
        else:
            print("\nChoix invalide. Recommencez !")
############################################







