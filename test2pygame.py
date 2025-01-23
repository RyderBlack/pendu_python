import pygame
from pygame.locals import *
import random

pygame.init()

fenetre = pygame.display.set_mode((640, 480))
fenetre.fill((255, 255, 255))

continuer = True
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lettre_utilisé = []#Liste des lettres utilisé
who = ['m', 'o', 'n', 'i', 'k', 'a']
are = 0
you = []
lettre_mot = []
lettre_fausse = []
dashImg = []#Case vide du mot
word = ""
perso = pygame.image.load("un_pendu.jpg").convert_alpha()# 108x400 px
perso2 = pygame.image.load("its_me.png").convert_alpha()
persoRect = perso.get_rect() #crée un rectangle autour d'une image
persoRect.topleft = (327, 120)#dimension du rectangle
persoRect2 = perso.get_rect() #crée un rectangle autour d'une image
persoRect2.topleft = (0, 0)#dimension du rectangle
police = pygame.font.Font(None, 35)#taille et police
NOIR = (0, 0, 0)
flag = 0
flag2 = 0
enter = 0

def showLines():
    for i in range (len(word)):
        dashImg.append(pygame.image.load('minus-sign.png'))
        fenetre.blit(dashImg[i], (1 * i * 40, 400))

def draw(lettre_fausse, x, y):
    for lettre4 in lettre_fausse:
        texte = police.render(lettre4, True, NOIR)
        if x > 600:
            y += 30
            x = 550
        fenetre.blit(texte, (x, y))
        pygame.draw.line(fenetre, NOIR, (x + 20, y), (x - 10, y + 25))
        if len(lettre_fausse) == 1:
            pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
        if len(lettre_fausse) == 2:
            pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
            pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
        if len(lettre_fausse) == 3:
            pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
            pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
            pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
        if len(lettre_fausse) == 4:
            pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
            pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
            pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
            pygame.draw.line(fenetre, NOIR, (350, 175), (370, 235))
        if len(lettre_fausse) == 5:
            pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
            pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
            pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
            pygame.draw.line(fenetre, NOIR, (350, 175), (370, 235))
            pygame.draw.line(fenetre, NOIR, (350, 240), (365, 300))
        if len(lettre_fausse) == 6:
            fenetre.blit(perso, persoRect)
        x += 25

with open('words.txt','r') as file:
    word_list = file.read().splitlines() # Dans le cas d'un fichier où il y a un mot par ligne
    word = random.choice(word_list)

print(word)
while continuer :
    for event in pygame.event.get():
        x = 550
        y = 100
        pygame.draw.line(fenetre, NOIR, (200, 335), (300, 335))
        pygame.draw.line(fenetre, NOIR, (200, 335), (200, 100))
        pygame.draw.line(fenetre, NOIR, (200, 100), (350, 100))
        pygame.draw.line(fenetre, NOIR, (350, 100), (350, 135))
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN: #Si une touche est enfoncé
            for letter in letters:
                if letter == event.unicode.lower():
                        for letter2 in lettre_utilisé:
                            if event.unicode.lower() == letter2 and (len(lettre_fausse) != 5 and event.unicode.lower() != who[are]):
                                print("lettre deja utilisé")
                                enter = 0
                                flag = 1
                                break
                        if flag == 0:
                            lettre_utilisé.append(event.unicode.lower())
                            fenetre.fill((255, 255, 255))
                            enter = 1
                        else :
                            flag = 0
                        if enter == 1:
                            if len(lettre_fausse) == 5 and event.unicode.lower() == who[are]:
                                draw(lettre_fausse, x, y)
                                you.append(event.unicode.lower())
                                are += 1
                                if len(who) == len(you):
                                    fenetre.blit(perso2, persoRect2)
                                    continuer = False
                                    pygame.display.update()
                                    pygame.time.wait(500)

                            elif letter in word:
                                print("yes")
                                lettre_mot.append(event.unicode.lower())
                                fenetre.fill((255, 255, 255))
                                draw(lettre_fausse, x, y)
                                
                            else:
                                you = []
                                lettre_fausse.append(event.unicode.lower())
                                draw(lettre_fausse, x, y)
                        else:
                            enter = 0
                        print("Vous avez tapé {}".format(event.unicode))
                        print(lettre_utilisé)
                        print(lettre_fausse)
                        print(lettre_mot)
                        print(you)
    showLines()
    pygame.display.update()#mise a jour de l'image a chaque fin de boucle
    if len(lettre_fausse) == 6:
        pygame.time.wait(3500)
        continuer = False
pygame.quit()