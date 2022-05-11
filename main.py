# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:32:00 2022

@author: Admin
"""

#imports

from tkinter import *
import numpy as np



#fonctions

def plateau():       #créer le plateau
    x1,y1,x2,y2=50,10,100,60;
    ite=0;
    while x1<450 and y1<410 :
        can.create_rectangle(x1,y1,x2,y2,fill='#C49A45')        #créer les cases
        ite,x1,x2=ite+1,x1+50,x2+50;
        if ite==8:          #passe à la ligne suivante
            y1,y2=y1+50,y2+50;
            ite,x1,x2=0,50,100;
    for i in range(8):          #créer les numéros
        can.create_text((25,30+i*50),text="%s"%(i+1))
        can.create_text((75+i*50,435),text="%s"%(i+1))
        
        
        
def grille():           #créer une liste de listes avec les coordonnées de chaque cases
    x3,y3,x4,y4=55,15,95,55;
    ite_ligne,ite_colonne=0,0;
    cases=[[55,15,95,55]];
    while x3<440 and y3<400 :
        ite_ligne,x3,x4=ite_ligne+1,x3+50,x4+50;
        if ite_ligne==8:
            y3,y4=y3+50,y4+50;
            ite_ligne,x3,x4=0,55,95;
            ite_colonne=ite_colonne+1;
        cases.append([x3,y3,x4,y4])
    return cases
   
 
    
def pion(ligne,colonne,player):         #créer un pion à l'emplacement donnée par la grille
    global cases,matrice
    if player==0:       #définit la couleur de la pièce
        color='white'
    else:
        color='black'
    matrice[ligne-1,colonne-1]=player       #modifie la matrice de jeu
    j=colonne-1+8*(ligne-1);        #donne la place de la case dans la liste grille
    rond=can.create_oval(cases[j][0],cases[j][1],cases[j][2],cases[j][3],fill=color)
    return rond
    


def point(click):       #fonction lier au click gauche
    global player,matrice,matrice_retour,last_gain,last_pion,label,color,choice,piece_played,cases,piece_gagnee,best_case,ordi,best_play,max_coeff
    matrice_retour=matrice.copy();      #créer une copie de la matrice pour faire des comparaisons et des retour en arrière
    ite_ligne,ite_colonne=0,0;
    for j in range(64):         #traverse toute la liste grille
        if ite_colonne==8:      #retient les coordonées de la case de la vérification
            ite_colonne=0;
            ite_ligne=ite_ligne+1;
        if click.x<=cases[j][2] and click.x>=cases[j][0] and click.y>=cases[j][1] and click.y<=cases[j][3]:     #vérifie si le click est dans la j-ème case
            matrice[ite_ligne,ite_colonne]=player;          #modifie la matrice de jeu
            last_gain=gain(ite_ligne+1,ite_colonne+1,player)        #créer les derniers gains
            if sum(sum(matrice_retour-matrice))==(2-player) or matrice_retour[ite_ligne,ite_colonne]!=2:        #annule le dernier mouvement si il est illégal
                if player==0:
                    color='white'
                else:
                    color='black'
                matrice=matrice_retour.copy()       #redonne l'ancienne matrice comme matrice de jeu
                label['text'] = "sorry %s, try again"%color
            else :
                last_pion=pion(ite_ligne+1,ite_colonne+1,player);       #créer une pièce à l'endroit jouer
                player=(player+1)%2;        #change de joueur
                piece_played=piece_played+1;        #retient le nombre de pièce jouer
                if player==0:
                    color='white'
                else:
                    color='black'
                label['text'] ="%s, do your best !"%color
                for element in choice:          #détruit les ronds rouges qui signalent les possibilités de jeu
                    can.delete(element)
                choice=possibility()        #affiche les nouvelles possibilités de jeux
                if ordi==1:         #vérifie si c'est l'ordi qui joue
                    ordi_simple(best_case,max_gain)          #fait jouer l'ordi
                if ordi==2:
                    ordi_hard(best_play,max_coeff)
        ite_colonne=ite_colonne+1;
    if len(choice)==0:          #passe le tour du joueur s'il ne peut pas jouer
        player=(player+1)%2;
        if player==0:
            color='white'
        else:
            color='black'
        label['text'] ="%s, double turn !"%color
        choice=possibility()
    if piece_played==64:        #message de fin de partie
        total_black=sum(sum(matrice));
        total_white=64-total_black;
        if total_black==total_white:
            label['text']="You were both equally wonderful <3"
        elif total_black<total_white:
            label['text']="Praise the white lord ! (B%s and W%s)"%(total_black, total_white)
        else :
            label['text']="Praise the black lord ! (B%s and W%s)"%(total_black, total_white)

            
    
    
    
def gain(ligne,colonne,player):         #calcule et affiche les pièces obtenues
    global matrice,piece_gagnee
    last_gain=[]        #liste avec les pièces changées
    t=0;
    ligne_matrice=ligne-1;          #adapte les lignes et colonnes d'entrée à celle de la matrice
    colonne_matrice=colonne-1;
    piece_gagnee=0
    while ligne_matrice!=0:                 #vérification nord
        ligne_matrice=ligne_matrice-1       #fais défiler la colonne de la matrice vers le haut
        if matrice[ligne_matrice,colonne-1]==2:     #s'arrête s'il y a une case vide
            break
        elif matrice[ligne_matrice,colonne-1]==player:      #s'arrête s'il y a une case possédée par le joueur
            for k in range(t):          #transforme toutes les pièces en pièce du joueur qui vien de jouer
                piece_gagnee=piece_gagnee+1         #retient le nombre de pièces obtenues grâce au dernier mouvement
                last_gain.append(pion(ligne_matrice+k+2,colonne,player))
            break
        t=t+1       #nombre de pièce à transformer 
    t=0;        #réinitialisation de la position
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while ligne_matrice!=7:                 #vérification sud
        ligne_matrice=ligne_matrice+1;
        if matrice[ligne_matrice,colonne-1]==2:
            break
        elif matrice[ligne_matrice,colonne-1]==player:
            for k in range(t):
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne_matrice-k,colonne,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while colonne_matrice!=0:                 #vérification ouest
        colonne_matrice=colonne_matrice-1;
        if matrice[ligne-1,colonne_matrice]==2:
            break
        elif matrice[ligne-1,colonne_matrice]==player:
            for k in range(t):
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne,colonne_matrice+k+2,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while colonne_matrice!=7:                 #vérification est
        colonne_matrice=colonne_matrice+1;
        if matrice[ligne-1,colonne_matrice]==2:
            break
        elif matrice[ligne-1,colonne_matrice]==player:
            for k in range(t):
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne,colonne_matrice-k,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while ligne_matrice!=0 and colonne_matrice!=0:                 #vérification N-O
        ligne_matrice=ligne_matrice-1;
        colonne_matrice=colonne_matrice-1;
        if matrice[ligne_matrice,colonne_matrice]==2:
            break
        elif matrice[ligne_matrice,colonne_matrice]==player:
            for k in range(t):
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne_matrice+k+2,colonne_matrice+k+2,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while ligne_matrice!=7 and colonne_matrice!=7:                 #vérification S-E
        ligne_matrice=ligne_matrice+1;
        colonne_matrice=colonne_matrice+1;
        if matrice[ligne_matrice,colonne_matrice]==2:
            break
        elif matrice[ligne_matrice,colonne_matrice]==player:
            for k in range(t):
                matrice[ligne_matrice-k,colonne_matrice-k]=player;
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne_matrice-k,colonne_matrice-k,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while ligne_matrice!=0 and colonne_matrice!=7:                 #vérification N-E
        ligne_matrice=ligne_matrice-1;
        colonne_matrice=colonne_matrice+1;
        if matrice[ligne_matrice,colonne_matrice]==2:
            break
        elif matrice[ligne_matrice,colonne_matrice]==player:
            for k in range(t):
                matrice[ligne_matrice+k,colonne_matrice-k]=player
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne_matrice+k+2,colonne_matrice-k,player))
            break
        t=t+1
    t=0;
    ligne_matrice=ligne-1;
    colonne_matrice=colonne-1;
    while ligne_matrice!=7 and colonne_matrice!=0:                 #vérification S-O
        ligne_matrice=ligne_matrice+1;
        colonne_matrice=colonne_matrice-1;
        if matrice[ligne_matrice,colonne_matrice]==2:
            break
        elif matrice[ligne_matrice,colonne_matrice]==player:
            for k in range(t):
                matrice[ligne_matrice-k,colonne_matrice+k]=player
                piece_gagnee=piece_gagnee+1
                last_gain.append(pion(ligne_matrice-k,colonne_matrice+k+2,player))
            break
        t=t+1
    return last_gain        #retourne la liste de pièces changées
       
 

def possibility():          #permet d'afficher les possibilités de jeu
    global cases,matrice,player,piece_gagnee,best_case,max_gain, max_coeff, best_play,matrice_coeff
    ite_ligne,ite_colonne=0,0;
    max_gain=0
    max_coeff=-100
    choice=[]       #créer une liste des options où on peut jouer 
    for j in range(64):         #fait défilier les cases pour la vérification
        matrice_retour=matrice.copy()       #permettra de revenir à la matrice d'origine
        if ite_colonne==8:      #retient les coordonnées de la case vérifiée
            ite_colonne=0;
            ite_ligne=ite_ligne+1;
        if matrice_retour[ite_ligne,ite_colonne]==2:        #permet de faire un tests sur les cases vides
            matrice[ite_ligne,ite_colonne]=player;          #changement nécessaire pour utiliser la fonction gain
            test=gain(ite_ligne+1,ite_colonne+1,player)     #retient les changements de la fonction gain
            if piece_gagnee!=0:         #créer un rond rouge sur la case si on peut jouer dessus
                if max_gain<piece_gagnee:
                    max_gain=piece_gagnee
                    best_case=[ite_ligne+1,ite_colonne+1]
                if max_coeff<matrice_coeff[ite_ligne,ite_colonne]:
                    max_coeff=matrice_coeff[ite_ligne,ite_colonne]
                    best_play=[ite_ligne+1,ite_colonne+1]
                choice.append(can.create_oval(cases[j][0],cases[j][1],cases[j][2],cases[j][3],fill='#C63F10'))
            matrice=matrice_retour.copy()       #revient à la matrice d'origine
            for element in test:        #efface les pièces déssinées par la fonction gain
                can.delete(element)
        ite_colonne=ite_colonne+1;
    return choice
    
                
        
def retour():       #permet de revenir au coup précédent
    global matrice,matrice_retour,player,choice,piece_played
    piece_played=piece_played-1;        #retire la pièce du total de pièces jouées
    matrice=matrice_retour.copy()       #revient à la matrice précédente qu'on a retenue dans la fonction point
    for element in last_gain:       #supprime les gains du coup précédent
        can.delete(element)
    can.delete(last_pion)       #supprime la dernière pièce jouée
    player=(player+1)%2;        #revient au joueur d'avant
    if player==0:
        color='white'
    else:
        color='black'
    label['text'] ="%s, do your best !"%color       #réécrit le bon message
    for element in choice:          #supprime les anciennes options de coup jouable
        can.delete(element)
    choice=possibility()        #réaffiche les possibilités de jeu
    
    
    
def play_PvP():         #met en place le jeu et les pièces de départ
    global matrice,piece_played,player,color,cases,choice,ordi,matrice_coeff
    player=1        #définit le premier joueur
    color='black'
    plateau()       #créer le terrain
    matrice=np.ones((8,8))*2;       #créer la matrice de jeu
    matrice_coeff=np.array([[1000,-40,50,-10,-10,50,-40,1000],
                           [-40,-50,-10,0,0,-10,-50,-40],
                           [50,-10,20,10,10,20,-10,50],
                           [-10,0,10,10,10,10,0,-10],
                           [-10,0,10,10,10,10,0,-10],
                           [50,-10,20,10,10,20,-10,50],
                           [-40,-50,-10,0,0,-10,-50,-40],
                           [1000,-40,50,-10,-10,50,-40,1000]])
    matrice[4,4]=0; matrice[3,3]=0; matrice[4,3]=1; matrice[3,4]=1;         #place les pions de départ dans la matrice
    piece_played=4;         #initialise le compte de pièces jouées
    pion(5,5,0)         #déssine les pièces de départ
    pion(4,4,0)
    pion(4,5,1)
    pion(5,4,1)
    choice=possibility()        #affiche les possibilités du premier joueur
    ordi=0
    
    
    
def ordi_simple(best_case,max_gain):
    global player,piece_played,choice
    if max_gain!=0 and piece_played!=64:        #vérifie que l'ordi peut effectivement jouer
        matrice[best_case[0]-1,best_case[1]-1]=0;          #modifiacation de la matrice
        pion(best_case[0],best_case[1],0);          #dessine la pièce de l'ordi
        gain(best_case[0],best_case[1],0)           #dessine les gains de l'ordi
        label['text'] ="black, do your best !"
        piece_played=piece_played+1;
        for element in choice:          #détruit les ronds rouges qui signalent les possibilités de jeu
            can.delete(element)
    else:
        label['text']="black, double turn !"
    player=(player+1)%2
    choice=possibility()
    
    
    
    
def play_simple():
    global ordi
    play_PvP()
    ordi=1      #active le premier ordi
    
    
    
def ordi_hard(best_play,max_coeff):
    global player,piece_played,choice
    if max_coeff!=-100 and piece_played!=64:        #vérifie que l'ordi peut effectivement jouer
        matrice[best_play[0]-1,best_play[1]-1]=0;          #modifiacation de la matrice
        pion(best_play[0],best_play[1],0);          #dessine la pièce de l'ordi
        gain(best_play[0],best_play[1],0)           #dessine les gains de l'ordi
        label['text'] ="black, do your best !"
        piece_played=piece_played+1;
        for element in choice:          #détruit les ronds rouges qui signalent les possibilités de jeu
            can.delete(element)
    else:
        label['text']="black, double turn !"
    player=(player+1)%2
    choice=possibility()    
                
            
def play_difficile():
    global ordi
    play_PvP()
    ordi=2
    

#fenêtre

window = Tk()       #créer une fenêtre
window.title("Othello")         #change le titre de la fenêtre
window.minsize(460,500)         #fixe la taille minimum
window.maxsize(460,500)         #fixe la taille maximum


#canvas

can=Canvas(window,width=460,heigh=460,bg="#088706")         #créer un panneau où placer les éléments visuels
can.pack(side=TOP)          #place le panneau dans la partie supérieur
plateau()       #affiche le plateau vide
cases=grille();         #crée les coordonnées des cases 
Button(window,text='Retour',command=retour).pack(side =LEFT)        #crée le boutton retour
label = Label(window, text="black, do your best !")         #initialise le premier message
label.pack(side=LEFT)
Button(window,text='Play PvP',command=play_PvP).pack(side=RIGHT)        #crée le boutton pour une partie à deux joueur
Button(window,text='Play hard',command=play_difficile).pack(side=RIGHT)
Button(window,text='Play simple',command=play_simple).pack(side=RIGHT)
can.bind('<Button-1>',point)        #permet de lier le click à la fonction point



window.mainloop()
