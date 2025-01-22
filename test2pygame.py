import pygame
from pygame.locals import *
import random

pygame.init()

fenetre = pygame.display.set_mode((640, 480))
fenetre.fill((255, 255, 255))

continuer = True
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lettre_utilisé = []#Liste des lettres utilisé
dashImg = []#Case vide du mot
word = ""
perso = pygame.image.load("un_pendu.jpg").convert_alpha()# 108x400 px
persoRect = perso.get_rect() #crée un rectangle autour d'une image
persoRect.topleft = (327, 120)#dimension du rectangle
police = pygame.font.Font(None, 35)#taille et police
NOIR = (0, 0, 0)
flag = 0

def showLines():
    for i in range (len(word)):
        dashImg.append(pygame.image.load('minus-sign.png'))
        fenetre.blit(dashImg[i], (1 * i * 40, 400))

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
                            if event.unicode.lower() == letter2:
                                print("lettre deja utilisé")
                                flag = 1
                                break
                        if flag == 0:
                            lettre_utilisé.append(event.unicode.lower())
                            fenetre.fill((255, 255, 255))
                        else :
                            flag = 0
                        print("Vous avez tapé {}".format(event.unicode))
                        print(lettre_utilisé)
                        for lettre in lettre_utilisé:
                            texte = police.render(lettre, True, NOIR)
                            if x > 600:
                                y += 30
                                x = 550
                            fenetre.blit(texte, (x, y))
                            pygame.draw.line(fenetre, NOIR, (x + 20, y), (x - 10, y + 25))
                            if len(lettre_utilisé) == 1:
                                pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
                            if len(lettre_utilisé) == 2:
                                pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
                                pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
                            if len(lettre_utilisé) == 3:
                                pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
                                pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
                                pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
                            if len(lettre_utilisé) == 4:
                                pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
                                pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
                                pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
                                pygame.draw.line(fenetre, NOIR, (350, 175), (370, 235))
                            if len(lettre_utilisé) == 5:
                                pygame.draw.circle(fenetre, NOIR, (350, 150), 20)
                                pygame.draw.line(fenetre, NOIR, (350, 150), (350, 240))
                                pygame.draw.line(fenetre, NOIR, (350, 175), (330, 235))
                                pygame.draw.line(fenetre, NOIR, (350, 175), (370, 235))
                                pygame.draw.line(fenetre, NOIR, (350, 240), (365, 300))
                            if len(lettre_utilisé) == 6:
                                fenetre.blit(perso, persoRect)
                                continuer = False
                            x += 25
    showLines()
    pygame.display.update()#mise a jour de l'image a chaque fin de boucle
    if len(lettre_utilisé) == 6:
        pygame.time.wait(4000)
pygame.quit()