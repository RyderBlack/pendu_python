import random
import pygame
from pygame.locals import *
import sys

pygame.init()
WIDTH, HEIGHT = 930, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échafaud")

# Charge le background
background = pygame.image.load("Background_HiRes2.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

 # Couleurs
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)

perso = pygame.image.load("un_pendu2.png").convert_alpha() # 108x400 px
persoRect = perso.get_rect() #crée un rectangle autour d'une image
persoRect.topleft = (327, 120) #dimension du rectangle

# perso = pygame.transform.scale(perso, (100, 200))  # Adjust based on your needs
# persoRect = perso.get_rect(center=(400, 310))

perso2 = pygame.image.load("its_me.png").convert_alpha()
persoRect2 = perso.get_rect() #crée un rectangle autour d'une image
persoRect2.topleft = (0, 0)#dimension du rectangle

police = pygame.font.Font(None, 35) #taille et police


class WordGame:
    def __init__(self):
        self.word_list = []
        self.chosen_word = ""
        self.life = 7
        self.score = 0
        self.x = 550
        self.y = 100
        
        self.is_running = True
        self.flag = 0
        self.flag2 = 0
        self.enter = 0
        self.lettre_utilisé = [] #Liste des lettres utilisé
        self.dashImg = [] #Case vide du mot
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.lettre_mot = []
        self.lettre_fausse = []
        self.x = 0
        self.y = 0
        
        self.who = ['m', 'o', 'n', 'i', 'k', 'a']
        self.are = 0
        self.you = []
        
        
        self.NOIR = (0, 0, 0)
        
    def store_words(self):
        with open('words.txt','r') as file:
            self.word_list = file.read().splitlines() # Dans le cas d'un fichier où il y a un mot par ligne
            self.chosen_word = random.choice(self.word_list)
            print(self.chosen_word)
            
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

    def show_lines(self):
        start_x = (WIDTH - (len(self.chosen_word) * 40)) // 2
        
        for i in range(len(self.chosen_word)):
            self.dashImg.append(pygame.image.load('minus-sign.png'))
            screen.blit(self.dashImg[i], (start_x + i * 40, 700))
            
            # To display the right letters on top of the lines
            for guessed_letter in self.lettre_mot:
                if guessed_letter in self.chosen_word:
                    
                    for position in range(len(self.chosen_word)):
                        current_letter = self.chosen_word[position]
                        
                        if current_letter == guessed_letter:
                            letter_render = police.render(guessed_letter, True, self.NOIR)
                            screen.blit(letter_render, (start_x + position * 42, 680))
                
    def draw(self):
        # Draw wrong guesses first
        self.x = 20 
        self.y = 20
        for lettre4 in self.lettre_fausse:
            texte = police.render(lettre4, True, self.NOIR)
            if self.x > WIDTH - 40:
                self.y += 30
                self.x = 20
            screen.blit(texte, (self.x, self.y))
            pygame.draw.line(screen, self.NOIR, (self.x + 20, self.y), 
                           (self.x - 10, self.y + 25))
            self.x += 25
        if len(self.lettre_fausse) >= 6:
        # Show final hangman image only
            scaled_perso = pygame.transform.scale(perso, (100, 160))
            perso_rect = scaled_perso.get_rect(midtop=(270, 440))
            screen.blit(scaled_perso, perso_rect)
        else:
            if len(self.lettre_fausse) >= 1:
                pygame.draw.circle(screen, self.NOIR, (270, 465), 20)  # Head
            if len(self.lettre_fausse) >= 2:
                pygame.draw.line(screen, self.NOIR, (270, 485), (270, 545), 5)  # Body
            if len(self.lettre_fausse) >= 3:
                pygame.draw.line(screen, self.NOIR, (270, 505), (230, 525), 5)  # Left arm
            if len(self.lettre_fausse) >= 4:
                pygame.draw.line(screen, self.NOIR, (270, 505), (310, 525), 5)  # Right arm
            if len(self.lettre_fausse) >= 5:
                pygame.draw.line(screen, self.NOIR, (270, 545), (240, 575), 5)  # Left leg
            if len(self.lettre_fausse) >= 6:
                pygame.draw.line(screen, self.NOIR, (270, 545), (300, 575), 5)  # Right leg
            

     
    #  ===== NOT YET IMPLEMENTED  =====
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
        3. Choix du mode
        """
        print(menu)      
    
    
    
class GameManager:
    def __init__(self):
        self.game = WordGame()

    def run(self):
        self.game.store_words()
        while self.game.is_running :
            for event in pygame.event.get():
                
                # arrière-plan vierge
                screen.blit(background, (0, 0))

                # L'échafaud
                pygame.draw.rect(screen, BROWN, (70, 600, 400, 20))  # Plateforme
                # Poteaux
                pygame.draw.rect(screen, BROWN, (90, 400, 20, 200))  # Poteau gauche
                pygame.draw.rect(screen, BROWN, (90, 380, 200, 20))  # Poutre horizontale
                # Pieds
                pygame.draw.rect(screen, BROWN, (70, 620, 20, 80))  # Pied gauche avant
                pygame.draw.rect(screen, BROWN, (450, 620, 20, 80))  # Pied droit avant
                pygame.draw.rect(screen, BROWN, (90, 620, 20, 80))  # Pied gauche arrière
                pygame.draw.rect(screen, BROWN, (430, 620, 20, 80))  # Pied droit arrière
                # Escalier
                for i in range(5):
                    pygame.draw.rect(screen, BROWN, (50, 620 + i * 20, 80, 10))
                # Corde
                pygame.draw.line(screen, GRAY, (270, 380), (270, 460), 5)  # Ligne de la corde
                pygame.draw.circle(screen, BLACK, (270, 470), 10)  # Noeud de la corde
                
                if event.type == QUIT:
                    self.game.is_running = False
                if event.type == KEYDOWN: #Si une touche est enfoncé
                    for letter in self.game.letters:
                        if letter == event.unicode.lower():
                                for letter2 in self.game.lettre_utilisé:
                                    if event.unicode.lower() == letter2 and (len(self.game.lettre_fausse) != 5 and event.unicode.lower() != self.game.who[self.game.are]):
                                        print("lettre deja utilisé")
                                        self.game.enter = 0
                                        self.game.flag = 1
                                        break
                                if self.game.flag == 0:
                                    self.game.lettre_utilisé.append(event.unicode.lower())
                                    self.game.enter = 1
                                else :
                                    self.game.flag = 0
                                
                                if self.game.enter == 1:
                                    # if letter in self.game.chosen_word:
                                    if len(self.game.lettre_fausse) == 5 and event.unicode.lower() == self.game.who[self.game.are]:
                                        self.game.draw()
                                        self.game.you.append(event.unicode.lower())
                                        self.game.are += 1
                                        if len(self.game.who) == len(self.game.you):
                                            screen.blit(perso2, persoRect2)
                                            self.game.is_running = False
                                            pygame.display.update()
                                            pygame.time.wait(500)
                                    elif letter in self.game.chosen_word:
                                        print("yes")
                                        self.game.lettre_mot.append(event.unicode.lower())
                                        print(f"ceci est {self.game.lettre_mot}")
                                        self.game.draw()
                                    else:
                                        print("Nope!")
                                        self.game.you
                                        self.game.lettre_fausse.append(event.unicode.lower())
                                        print(f"ceci est {self.game.lettre_mot}")
                                        self.game.draw()
                                else:
                                    self.enter = 0
                                print("Vous avez tapé {}".format(event.unicode))
                                print(self.game.lettre_utilisé)

                                print(self.game.lettre_fausse)
                                print(self.game.lettre_mot)
                                print(self.game.you)
            self.game.draw()         
            self.game.show_lines()
            pygame.display.flip() #mise a jour de l'image a chaque fin de boucle
            if len(self.game.lettre_fausse) == 6:
                pygame.time.wait(3500)
                self.game.is_running = False
        pygame.quit()
        sys.exit

        # while True:
        #     try:
                
        #         self.game.display_menu()
        #         self.game.store_words()
                
        #         user_choice = input("Entrez votre choix: ")
                
        #         if user_choice == "1":
        #             self.game.shuffle_words()
        #             self.game.show_lines()
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
    
    
    