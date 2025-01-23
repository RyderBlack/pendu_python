import random
import pygame
from pygame.locals import *


fenetre = pygame.display.set_mode((640, 480))
fenetre.fill((255, 255, 255))



letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lettre_utilisé = [] #Liste des lettres utilisé
dashImg = [] #Case vide du mot
word = ""
perso = pygame.image.load("un_pendu.jpg").convert_alpha() # 108x400 px
persoRect = perso.get_rect() #crée un rectangle autour d'une image
persoRect.topleft = (327, 120) #dimension du rectangle
pygame.font.init()
police = pygame.font.Font(None, 35) #taille et police




class WordGame:
    def __init__(self):
        self.word_list = []
        self.chosen_word = ""
        self.life = 7
        self.score = 0
        self.continuer = True
        self.flag = 0
        
        self.NOIR = (0, 0, 0)
        
    def store_words(self):
        with open('words.txt','r') as file:
            self.word_list = file.read().splitlines() # Dans le cas d'un fichier où il y a un mot par ligne
            self.chosen_word = random.choice(self.word_list)
            
    def add_word(self):
        added_word = input("entrez votre mot: ").lower()
        
        if added_word in self.word_list:
                print(f"Le mot {added_word} est déjà dans la liste, merci d'en choisir un autre.")          
        else:
            self.word_list.append(added_word)
            word_file = open("words.txt", "a")
            word_file.write("\n"+added_word)
            word_file.close()
            print(f"Ajout du mot {self.word_list[-1]} à la base de donnée.")
        
    def shuffle_words(self):
        random.shuffle(self.word_list)
        self.chosen_word = self.word_list[0]
        print(f"Le mot choisi est: {self.chosen_word}")
        return self.chosen_word

    def display_hints(self):
        for i in range(len(self.chosen_word)):
            length_hint = len(self.chosen_word)
            print("_" * length_hint)
            dashImg.append(pygame.image.load('minus-sign.png'))
            fenetre.blit(dashImg[i], (1 * i * 40, 400))
        
    def guess_the_word(self):
        while True:
            letter_box = []
            letter = input("Devine une lettre: ")
            if letter in self.chosen_word:
                print(f"GG! la lettre {letter} est bien dans le mot à deviner!")
                self.score += 1
                print(f"Ton score est maintenant de {self.score}")
                letter_box.append(letter)
                
                if self.score == len(self.chosen_word):
                    print("OMG! T'as gagné la game!")
                    break
                
                elif letter in letter_box:
                    print("Cette lettre a déjà été devinée")
                    print(f"le score est toujours de {self.score}")
                
            
            else: 
                self.life -= 1
                print("Nope! image N du pendu ici")
                print(self.life)
                if self.life == 0:
                    print("déso mais t'as perdu!")
                    break
    
    @staticmethod
    def display_menu():
        menu = """
        1. Jouer
        2. Ajouter un nouveau mot
        """
        print(menu)      
    
    
    
class GameManager:
    def __init__(self):
        self.game = WordGame()

    def run(self):
        while self.game.continuer :
            for event in pygame.event.get():
                x = 550
                y = 100
                pygame.draw.line(fenetre, self.game.NOIR, (200, 335), (300, 335))
                pygame.draw.line(fenetre, self.game.NOIR, (200, 335), (200, 100))
                pygame.draw.line(fenetre, self.game.NOIR, (200, 100), (350, 100))
                pygame.draw.line(fenetre, self.game.NOIR, (350, 100), (350, 135))
                if event.type == QUIT:
                    self.game.continuer = False
                if event.type == KEYDOWN: #Si une touche est enfoncé
                    for letter in letters:
                        if letter == event.unicode.lower():
                                for letter2 in lettre_utilisé:
                                    if event.unicode.lower() == letter2:
                                        print("lettre deja utilisé")
                                        self.game.flag = 1
                                        break
                                if self.game.flag == 0:
                                    lettre_utilisé.append(event.unicode.lower())
                                    fenetre.fill((255, 255, 255))
                                else :
                                    self.game.flag = 0
                                print("Vous avez tapé {}".format(event.unicode))
                                print(lettre_utilisé)
                                for lettre in lettre_utilisé:
                                    texte = police.render(lettre, True, self.game.NOIR)
                                    if x > 600:
                                        y += 30
                                        x = 550
                                    fenetre.blit(texte, (x, y))
                                    pygame.draw.line(fenetre, self.game.NOIR, (x + 20, y), (x - 10, y + 25))
                                    if len(lettre_utilisé) == 1:
                                        pygame.draw.circle(fenetre, self.game.NOIR, (350, 150), 20)
                                    if len(lettre_utilisé) == 2:
                                        pygame.draw.circle(fenetre, self.game.NOIR, (350, 150), 20)
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 150), (350, 240))
                                    if len(lettre_utilisé) == 3:
                                        pygame.draw.circle(fenetre, self.game.NOIR, (350, 150), 20)
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 150), (350, 240))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 175), (330, 235))
                                    if len(lettre_utilisé) == 4:
                                        pygame.draw.circle(fenetre, self.game.NOIR, (350, 150), 20)
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 150), (350, 240))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 175), (330, 235))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 175), (370, 235))
                                    if len(lettre_utilisé) == 5:
                                        pygame.draw.circle(fenetre, self.game.NOIR, (350, 150), 20)
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 150), (350, 240))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 175), (330, 235))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 175), (370, 235))
                                        pygame.draw.line(fenetre, self.game.NOIR, (350, 240), (365, 300))
                                    if len(lettre_utilisé) == 6:
                                        fenetre.blit(perso, persoRect)
                                        self.game.continuer = False
                                    x += 25
            self.game.display_hints()
            pygame.display.update()#mise a jour de l'image a chaque fin de boucle
            if len(lettre_utilisé) == 6:
                pygame.time.wait(4000)
        pygame.quit()

        # while True:
        #     try:
                
        #         self.game.display_menu()
        #         self.game.store_words()
                
        #         user_choice = input("Entrez votre choix: ")
                
        #         if user_choice == "1":
        #             self.game.shuffle_words()
        #             self.game.display_hints()
        #             # self.game.guess_the_word()
        #         elif user_choice == "2":    
        #             self.game.add_word()
        #         else:
        #             print("Merci de faire un choix entre 1 et 2.")
            
        #     except KeyboardInterrupt:
        #         print("\nMerci d'avoir joué!")
        #         break


def main():
    game_manager = GameManager()
    game_manager.run()
        
if __name__ == "__main__":
    main() 
    
    
    