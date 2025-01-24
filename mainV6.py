import random
import pygame
from pygame.locals import *
import sys

# pygame init and screen 
pygame.init()
WIDTH, HEIGHT = 930, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échafaud")
background = pygame.image.load("Background_HiRes2.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# COLORS
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)

# Secret ending asset if failed game
perso = pygame.image.load("un_pendu2.png").convert_alpha() # 108x400 px
persoRect = perso.get_rect() #crée un rectangle autour d'une image
persoRect.topleft = (450, 420) #dimension du rectangle

# Secret ending asset for hardcore mode
perso2 = pygame.image.load("its_me.png").convert_alpha()
persoRect2 = perso.get_rect() 
persoRect2.topleft = (0, 0) 

# FONT & TEXT
police = pygame.font.Font(None, 35)
font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255,255,255)

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
    
 
# Main Game Class   
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
        self.lettre_utilisé = []
        self.dashImg = []
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.lettre_mot = []
        self.lettre_fausse = []
        self.x = 0
        self.y = 0
        
        self.who = ['m', 'o', 'n', 'i', 'k', 'a']
        self.are = 0
        self.you = []
        
        self.NOIR = (0, 0, 0)
    
    #store the words.txt words and choose a random one    
    def store_words(self):
        with open('words.txt','r') as file:
            self.word_list = file.read().splitlines()
            self.chosen_word = random.choice(self.word_list)
            print(self.chosen_word)
    
    # display an input screen and add a new word in word_list AND in words.txt file       
    def add_word(self):
        added_word = ""
        greeting_text = "Bienvenue! Entrez un nouveau mot et appuyez sur Entrée :"
        input_box = pygame.Rect(10, 60, 500, 100)
        active_color = (0, 205, 0) 
        inactive_color = (200, 200, 200) 
        input_box_color = inactive_color
        background_color = (30, 30, 30) 
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    input_box_color = active_color 
                    if event.key == pygame.K_RETURN:
                        if added_word.strip():
                            if added_word in self.word_list:
                                print(f"Le mot '{added_word}' est déjà dans la liste, merci d'en choisir un autre.")
                            else:
                                self.word_list.append(added_word)
                                with open("words.txt", "a") as word_file:
                                    word_file.write("\n" + added_word)
                                print(f"Ajout du mot '{added_word}' à la base de données.")
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        added_word = added_word[:-1]
                    elif event.unicode.isalpha():  # isalpha is for only alphabetic characters !
                        added_word += event.unicode.lower()

            screen.fill(background_color)  
            greeting_font = pygame.font.SysFont("arial", 30)
            greeting_surface = greeting_font.render(greeting_text, True, (255, 255, 255))
            screen.blit(greeting_surface, (10, 10))

            pygame.draw.rect(screen, input_box_color, input_box, 2) 
            input_surface = font.render(added_word, True, (255, 255, 255))
            screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            pygame.display.flip()
            
    # Display the lines below the letters and show guessed letters as well
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
    
    # Draw the full hangman body            
    def draw(self):
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
            
        # To display secret asset #1
        if len(self.lettre_fausse) >= 6:
            screen.blit(perso, persoRect)
            
        # Display the hangman body parts HERE    
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
    
    # VICTORY SCREEN
    def show_victory_screen(self):
        victory_message = "Victoire ! Félicitations !"
        self.display_end_screen(victory_message, (0, 255, 0))  

    # DEFEAT SCREEN
    def show_defeat_screen(self):
        defeat_message = "Défaite ! Vous avez perdu !"
        self.display_end_screen(defeat_message, (255, 0, 0)) 

    # Display an ending screen either if victory or defeat
    def display_end_screen(self, message, text_color):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        self.lettre_utilisé = []
                        self.lettre_mot = []
                        self.lettre_fausse = []
                        self.dashImg = []
                       
                        self.chosen_word = random.choice(self.word_list)
                        return True # Restart
                    elif event.key == pygame.K_ESCAPE:  
                        return False # Quit
            
            screen.fill((0, 0, 0))

            message_font = pygame.font.SysFont("arial", 60)
            message_surface = message_font.render(message, True, text_color)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(message_surface, message_rect)

            instructions = "Appuyez sur Entrée pour recommencer ou sur Échap pour quitter"
            instructions_font = pygame.font.SysFont("arial", 30)
            instructions_surface = instructions_font.render(instructions, True, (255, 255, 255))
            instructions_rect = instructions_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(instructions_surface, instructions_rect)

            word_text = f"Le mot était : {self.chosen_word}"
            word_surface = instructions_font.render(word_text, True, (255, 255, 255))
            word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            screen.blit(word_surface, word_rect)

            pygame.display.flip()


# Button class for the menu items
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
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
  
   
# Buttons images

# resume
resume_img = pygame.image.load("./images/buttons/Button_continuer.png").convert_alpha()
resume_button = Button(300,150, resume_img, 0.5) 

# jouer
play_img = pygame.image.load("./images/buttons/Button_jouer.png").convert_alpha()
play_button = Button(300,20, play_img, 0.5) 

# options
options_img = pygame.image.load("./images/buttons/Button_options.png").convert_alpha()
options_button = Button(300,220, options_img, 0.5) 

#  difficulty
# difficulty_img = pygame.image.load("./images/buttons/Button_difficulty.png").convert_alpha()
# difficulty_button = Button(300,350, difficulty_img, 0.5) 

#  add_word
add_word_img = pygame.image.load("./images/buttons/Button_add_word.png").convert_alpha()
add_word_button = Button(300,420, add_word_img, 0.5) 

#  audio
audio_img = pygame.image.load("./images/buttons/Button_audio.png").convert_alpha()
audio_button = Button(300,150, audio_img, 0.5) 

# go back
retour_img = pygame.image.load("./images/buttons/Button_retour.png").convert_alpha()
retour_button = Button(300,350, retour_img, 0.5) 

# quit
quit_img = pygame.image.load("./images/buttons/Button_quitter.png").convert_alpha()
quit_button = Button(300,620, quit_img, 0.5) 
   
   
# Main Class to run the game    
class GameManager:
    def __init__(self):
        self.game = WordGame()
        self.game_paused = True
        self.menu_state = "main"
        
    def run(self):

        self.game.store_words()
        while self.game.is_running :
            
            # The First BG
            screen.blit(background, (0, 0))
            
            # The menu logic here
            if self.game_paused == True:
                #  check menu state
                if self.menu_state == "main":
                    
                    if play_button.draw(screen): 
                        self.menu_state = "play"               
                        self.game_paused = False   
                        self.reset_game()      
                    if add_word_button.draw(screen):
                        self.game.add_word() 
                    if options_button.draw(screen):
                        self.menu_state = "options"
                    if quit_button.draw(screen):
                        pygame.quit()
                        sys.exit()
                        
                if self.menu_state == "options":
                    if audio_button.draw(screen):
                        print("change audio here")
                    if retour_button.draw(screen):
                        self.menu_state = "main"
                        
                if self.menu_state == "play":
                    # if screen.blit(background, (0, 0)):
                    #     pass
                    if retour_button.draw(screen):
                        self.menu_state = "main"
                        self.game_paused = True
                        
            # GAME LOGIC HERE
            else:   
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
                
                pygame.display.flip() # To update the screen after each loop

                
            # Event Handling / Keys pressed
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                
                if event.type == QUIT:
                    # self.game.is_running = False
                    pygame.quit()
                    sys.exit()
                
                
                # CHECK VICTORY OR DEFEAT HERE
                if self.game.life <= 0:
                    result = self.game.show_defeat_screen() 
                elif set(self.game.chosen_word) == set(self.game.lettre_mot):
                    result = self.game.show_victory_screen() 
                else:
                    result = None

                if result == True: 
                    self.game_paused = True 
                    self.menu_state = "main" 
                elif result == False:  
                    pygame.quit()
                    sys.exit()
                
                
                # Keyboard letters during game
                if event.type == KEYDOWN:
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
                                    # print(f"ceci est {self.game.lettre_mot}")
                                    self.game.draw()
                                    
                                else:
                                    print("Nope!")
                                    self.game.you
                                    self.game.lettre_fausse.append(event.unicode.lower())
                                    # print(f"ceci est {self.game.lettre_mot}")
                                    self.game.draw()
                            else:
                                self.enter = 0
                            # print("Vous avez tapé {}".format(event.unicode))
                            # print(self.game.lettre_utilisé)
                            # print(self.game.lettre_fausse)
                            # print(self.game.lettre_mot)
                            # print(self.game.you)
                          
            pygame.display.update()
        pygame.quit()
        sys.exit
    
    def reset_game(self):
        self.game.lettre_utilisé = []  
        self.game.lettre_mot = []     
        self.game.lettre_fausse = [] 
        self.game.dashImg = []       
        self.game.life = 7           
        self.game.store_words()      
    

# Main function to trigger the GameManager and whole program
def main():
    game_manager = GameManager()
    game_manager.run()
        
if __name__ == "__main__":
    main() 
    
    
    