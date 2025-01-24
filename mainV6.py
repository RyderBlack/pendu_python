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
persoRect.topleft = (450, 420) #dimension du rectangle

#perso = pygame.transform.scale(perso, (80, 200))  # Adjust based on your needs
#persoRect = perso.get_rect(center=(400, 310))

perso2 = pygame.image.load("its_me.png").convert_alpha()
persoRect2 = perso.get_rect() #crée un rectangle autour d'une image
persoRect2.topleft = (0, 0)#dimension du rectangle

police = pygame.font.Font(None, 35) #taille et police
font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255,255,255)

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
    
    
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
        added_word = ""
        greeting_text = "Bienvenue! Entrez un nouveau mot et appuyez sur Entrée :"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Handle Enter key
                        if added_word.strip():  # Ensure the word is not empty
                            if added_word in self.word_list:
                                print(f"Le mot '{added_word}' est déjà dans la liste, merci d'en choisir un autre.")
                            else:
                                self.word_list.append(added_word)
                                with open("words.txt", "a") as word_file:
                                    word_file.write("\n" + added_word)
                                print(f"Ajout du mot '{added_word}' à la base de données.")
                            return  # Exit the function after adding the word
                    elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                        added_word = added_word[:-1]
                    elif event.unicode.isalpha():  # Only allow alphabetic characters
                        added_word += event.unicode.lower()

            # Draw the screen
            screen.fill((0, 0, 0))  # Clear the screen with a black background

            # Render the greeting text
            greeting_surface = font.render(greeting_text, True, (255, 255, 255))
            screen.blit(greeting_surface, (10, 10))

            # Render the user's input
            input_surface = font.render(added_word, True, (255, 255, 255))
            screen.blit(input_surface, (10, 60))

            pygame.display.flip()

    def show_lines(self):
        start_x = (WIDTH - (len(self.chosen_word) * 40)) // 2
        
        for i in range(len(self.chosen_word)):
            self.dashImg.append(pygame.image.load('minus-sign.png'))
            screen.blit(self.dashImg[i], (start_x + i * 40, 300))
            
            # To display the right letters on top of the lines
            for guessed_letter in self.lettre_mot:
                if guessed_letter in self.chosen_word:
                    
                    for position in range(len(self.chosen_word)):
                        current_letter = self.chosen_word[position]
                        
                        if current_letter == guessed_letter:
                            letter_render = police.render(guessed_letter, True, self.NOIR)
                            screen.blit(letter_render, (start_x + position * 42, 280))
                
    def draw(self):
        # Draw wrong guesses first
        self.x = 50 
        self.y = 50
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
            screen.blit(perso, persoRect)
            
        else:
            if len(self.lettre_fausse) >= 1:
                pygame.draw.circle(screen, self.NOIR, (470, 465), 15)  # Head
            if len(self.lettre_fausse) >= 2:
                pygame.draw.line(screen, self.NOIR, (470, 480), (470, 540), 5)  # Body
            if len(self.lettre_fausse) >= 3:
                pygame.draw.line(screen, self.NOIR, (470, 500), (430, 520), 5)  # Left arm
            if len(self.lettre_fausse) >= 4:
                pygame.draw.line(screen, self.NOIR, (470, 500), (510, 520), 5)  # Right arm
            if len(self.lettre_fausse) >= 5:
                pygame.draw.line(screen, self.NOIR, (470, 540), (440, 570), 5)  # Left leg
            if len(self.lettre_fausse) >= 6:
                pygame.draw.line(screen, self.NOIR, (470, 540), (500, 570), 5)  # Right leg
    
    
    # def main_game_logic(self):
    #     for event in pygame.event.get():
    #         for letter in self.letters:
    #             if letter == event.unicode.lower():
    #                 for letter2 in self.game.lettre_utilisé:
    #                     if event.unicode.lower() == letter2 and (len(self.lettre_fausse) != 5 and event.unicode.lower() != self.who[self.are]):
    #                         print("lettre deja utilisé")
    #                         self.enter = 0
    #                         self.flag = 1
    #                         break
    #                 if self.flag == 0:
    #                     self.lettre_utilisé.append(event.unicode.lower())
    #                     self.enter = 1
    #                 else :
    #                     self.flag = 0
                    
    #                 if self.enter == 1:
    #                     # if letter in self.game.chosen_word:
    #                     if len(self.lettre_fausse) == 5 and event.unicode.lower() == self.who[self.are]:
    #                         self.draw()
    #                         self.you.append(event.unicode.lower())
    #                         self.are += 1
    #                         if len(self.who) == len(self.you):
    #                             screen.blit(perso2, persoRect2)
    #                             GameManager().is_running = False
    #                             pygame.display.update()
    #                             pygame.time.wait(500)
    #                     elif letter in self.chosen_word:
    #                         print("yes")
    #                         self.lettre_mot.append(event.unicode.lower())
    #                         print(f"ceci est {self.lettre_mot}")
    #                         self.draw()
    #                     else:
    #                         print("Nope!")
    #                         self.you
    #                         self.lettre_fausse.append(event.unicode.lower())
    #                         print(f"ceci est {self.lettre_mot}")
    #                         self.draw()
    #                 else:
    #                     self.enter = 0
    #                 print("Vous avez tapé {}".format(event.unicode))
    #                 print(self.lettre_utilisé)

    #                 print(self.lettre_fausse)
    #                 print(self.lettre_mot)
    #                 print(self.you)        

     
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

class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        
        #  check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
  
# button images

# resume
resume_img = pygame.image.load("./images/buttons/Button_continuer.png").convert_alpha()
resume_button = Button(300,150, resume_img, 0.5) 

# jouer
play_img = pygame.image.load("./images/buttons/Button_jouer.png").convert_alpha()
play_button = Button(300,50, play_img, 0.5) 

# options
options_img = pygame.image.load("./images/buttons/Button_options.png").convert_alpha()
options_button = Button(300,250, options_img, 0.5) 

#  difficulty
# difficulty_img = pygame.image.load("./images/buttons/Button_difficulty.png").convert_alpha()
# difficulty_button = Button(300,350, difficulty_img, 0.5) 

#  add_word
add_word_img = pygame.image.load("./images/buttons/Button_add_word.png").convert_alpha()
add_word_button = Button(300,450, add_word_img, 0.5) 

#  audio
audio_img = pygame.image.load("./images/buttons/Button_audio.png").convert_alpha()
audio_button = Button(300,150, audio_img, 0.5) 

# go back
retour_img = pygame.image.load("./images/buttons/Button_retour.png").convert_alpha()
retour_button = Button(300,350, retour_img, 0.5) 

# quit
quit_img = pygame.image.load("./images/buttons/Button_quitter.png").convert_alpha()
quit_button = Button(300,650, quit_img, 0.5) 
    
class GameManager:
    def __init__(self):
        self.game = WordGame()
        self.game_paused = True
        self.menu_state = "main"
        
    def run(self):

        self.game.store_words()
        while self.game.is_running :
            
            # screen.fill((52,78,91))
            # arrière-plan vierge
            screen.blit(background, (0, 0))
            
            if self.game_paused == True:
                #  check menu state
                if self.menu_state == "main":
                    if play_button.draw(screen): 
                        self.menu_state = "play"               
                        self.game_paused = False
                        
                    if add_word_button.draw(screen):
                        self.game.add_word() 
                        
                    if options_button.draw(screen):
                        self.menu_state = "options"
                    if quit_button.draw(screen):
                        self.game.is_running = False
                if self.menu_state == "options":
                    if audio_button.draw(screen):
                        print("change audio here")
                    if retour_button.draw(screen):
                        self.menu_state = "main"
                if self.menu_state == "play":
                    if screen.blit(background, (0, 0)):
                        pass
                    if retour_button.draw(screen):
                        self.menu_state = "main"
                        self.game_paused = True
            else:
                # GAME LOGIC HERE
                # draw_text("Press SPACE to pause", font, TEXT_COL, 250, 350)
                # L'échafaud
                pygame.draw.rect(screen, BROWN, (250, 600, 400, 20))  # Plateforme
                # Poteaux
                pygame.draw.rect(screen, BROWN, (250, 400, 20, 200))  # Poteau gauche
                pygame.draw.rect(screen, BROWN, (250, 380, 250, 20))  # Poutre horizontale
                # Pieds
                pygame.draw.rect(screen, BROWN, (320, 620, 20, 80))  # Pied gauche avant
                pygame.draw.rect(screen, BROWN, (630, 620, 20, 80))  # Pied droit avant
                pygame.draw.rect(screen, BROWN, (250, 620, 20, 80))  # Pied gauche arrière
                pygame.draw.rect(screen, BROWN, (580, 620, 20, 80))  # Pied droit arrière
                # Escalier
                for i in range(5):
                    pygame.draw.rect(screen, BROWN, (220, 620 + i * 20, 80, 10))
                # Corde
                pygame.draw.line(screen, GRAY, (470, 380), (470, 460), 5)  # Ligne de la corde
                pygame.draw.circle(screen, BLACK, (470, 470), 10)  # Noeud de la corde
                self.game.draw()         
                self.game.show_lines()
                pygame.display.flip() #mise a jour de l'image a chaque fin de boucle
                if len(self.game.lettre_fausse) == 6:
                    pygame.time.wait(3000)
                    self.game.is_running = False
                
            
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                
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
                
                
            pygame.display.update()
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
    
    
    