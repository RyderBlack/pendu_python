import random
import pygame
from pygame.locals import *
import sys

# pygame init, screen and music
pygame.init()
# pygame.mixer.init()
pygame.mixer.init()

WIDTH, HEIGHT = 930, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échafaud")
background = pygame.image.load("./images/Background_HiRes2.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load Background music




# COLORS
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)

# Secret ending asset if failed game
perso = pygame.image.load("./images/un_pendu2.png").convert_alpha() # 108x400 px
persoRect = perso.get_rect() # draw a rectangle around image
persoRect.topleft = (450, 420) # size of rectangle

# Secret ending asset for hardcore mode
perso2 = pygame.image.load("./images/its_me.png").convert()
perso2_scaled = pygame.transform.scale(perso2, (930,800))



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
        self.sonor_effect = pygame.mixer.Sound('./audios/applause.mp3')
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
            self.chosen_word = random.choice(self.word_list).strip()
            print(self.chosen_word.strip())
    
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
            self.dashImg.append(pygame.image.load('./images/minus-sign.png'))
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
            if len(self.lettre_fausse) >= 7:
                clear_rect = pygame.Rect(430, 450, 130, 130)
                screen.blit(background.subsurface(clear_rect), clear_rect)
                pygame.draw.line(screen, GRAY, (470, 380), (470, 460), 5) 
                screen.blit(perso, persoRect)
                
 
            # Display the hangman body parts HERE    
            else:
                if len(self.lettre_fausse) >= 1:
                    pygame.draw.line(screen, GRAY, (470, 380), (470, 460), 5)  # Rope line
                    # pygame.draw.circle(screen, BLACK, (470, 470), 10)  # Rope knot    
                if len(self.lettre_fausse) >= 2:
                    pygame.draw.circle(screen, self.NOIR, (470, 465), 15)  # Head
                if len(self.lettre_fausse) >= 3:
                    pygame.draw.line(screen, self.NOIR, (470, 480), (470, 540), 5)  # Body
                if len(self.lettre_fausse) >= 4:
                    pygame.draw.line(screen, self.NOIR, (470, 500), (430, 520), 5)  # Left arm
                if len(self.lettre_fausse) >= 5:
                    pygame.draw.line(screen, self.NOIR, (470, 500), (510, 520), 5)  # Right arm
                if len(self.lettre_fausse) >= 6:
                    pygame.draw.line(screen, self.NOIR, (470, 540), (440, 570), 5)  # Left leg
                
                if len(self.lettre_fausse) >= 7:
                    pygame.draw.line(screen, self.NOIR, (470, 540), (500, 570), 5)  # Right leg
                
    
    
    # VICTORY SCREEN
    def show_victory_screen(self):
        pygame.time.wait(100)
        pygame.mixer.music.stop()
        main_music = pygame.mixer.Sound('./audios/gagnant.mp3')
        main_music.play(-1)  # Boucle infinie pour la musique principale
        self.sonor_effect.play()
        victory_message = "Victoire ! Félicitations !"
        self.display_end_screen(victory_message, (0, 255, 0))  
        main_music.stop()
        

    # DEFEAT SCREEN
    def show_defeat_screen(self):
         pygame.time.wait(1000)
         pygame.mixer.music.stop()
         pygame.mixer.music.load('./audios/perdant.mp3')
         pygame.mixer.music.play(-1)
         defeat_message = "defaite ! Paix a ton ame"
         self.display_end_screen(defeat_message, (255, 0, 0))
         
         pygame.mixer.music.stop()
        
        
        

    # Display an ending screen either if victory or defeat
    def display_end_screen(self, message, text_color):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        self.sonor_effect.stop()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('./audios/ost.mp3')
                        
                        pygame.mixer.music.play(-1)
                      
                        
                        self.lettre_utilisé = []
                        self.lettre_mot = []
                        self.lettre_fausse = []
                        self.dashImg = []
                       
                        self.chosen_word = random.choice(self.word_list)
                        return True # Restart
                    elif event.key == pygame.K_ESCAPE:  
                        pygame.quit()
                        sys.exit()
                        return False # Quit
                    
            
            screen.fill((0, 0, 0))

            message_font = pygame.font.SysFont("arialblack", 50)
            message_surface = message_font.render(message, True, text_color)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(message_surface, message_rect)

            instructions = "Appuyez sur Entrée pour revenir au menu ou sur Échap pour quitter"
            instructions_font = pygame.font.SysFont("arialblack", 20)
            instructions_surface = instructions_font.render(instructions, True, (255, 255, 255))
            instructions_rect = instructions_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(instructions_surface, instructions_rect)

            word_text = f"Le mot était : {self.chosen_word}"
            word_surface = instructions_font.render(word_text, True, (255, 255, 255))
            word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            screen.blit(word_surface, word_rect)

            pygame.display.flip()


class AnimatedCrowd():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shirt_color = ""
        self.pants_color = ""
        
        self.start_x = 30
        self.start_y = 750
        self.audience_base_x = 10
        self.audience_base_y = 550
        self.rows = 3
        self.cols = 40
        self.spacing = 24
        self.max_movement = 3
        
        self.animations = [[0, 0] for _ in range(self.rows * self.cols)]
        self.colors = [
        ((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),  # Chemise
         (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))   # Pantalon
        for _ in range(self.rows * self.cols)]
        
        
    def draw_character(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 10)  # Head

        # Body (shirt)
        pygame.draw.line(screen, self.shirt_color, (self.x, self.y + 10), (self.x, self.y + 40), 5)  # Body

        # Arms (Black)
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y + 15), (self.x - 10, self.y + 30), 3)  # Left Arm
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y + 15), (self.x + 10, self.y + 30), 3)  # Right Arm

        # Legs (colored)
        pygame.draw.line(screen, self.pants_color, (self.x, self.y + 40), (self.x - 10, self.y + 60), 3)  # Jambe gauche
        pygame.draw.line(screen, self.pants_color, (self.x, self.y + 40), (self.x + 10, self.y + 60), 3)  # Jambe droite

    def draw_audience(self):
        # Draw a crowd in several rows with animated movements
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                x_animation = self.animations[index][0]
                y_animation = self.animations[index][1]
                self.x = self.start_x + col * self.spacing + x_animation
                self.y = self.start_y - row * self.spacing + y_animation
                self.shirt_color, self.pants_color = self.colors[index]
                self.draw_character()

    def update_animations(self):
        # Randomize crowd movements
        for i in range(len(self.animations)):
            self.animations[i][0] += random.uniform(-0.5, 0.5)  # Horizontal movement 
            self.animations[i][1] += random.uniform(-0.5, 0.5)  # Vertical movement

            # Limit movements
            self.animations[i][0] = max(-self.max_movement, min(self.max_movement, self.animations[i][0]))
            self.animations[i][1] = max(-self.max_movement, min(self.max_movement, self.animations[i][1]))



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

# jouer
play_img = pygame.image.load("./images/buttons/Button_jouer.png").convert_alpha()
play_button = Button(300,100, play_img, 0.5) 

#  add_word
add_word_img = pygame.image.load("./images/buttons/Button_add_word.png").convert_alpha()
add_word_button = Button(300,350, add_word_img, 0.5) 

# quit
quit_img = pygame.image.load("./images/buttons/Button_quitter.png").convert_alpha()
quit_button = Button(300,600, quit_img, 0.5) 
   
   
# Main Class to run the game    
class GameManager:
    def __init__(self):
        self.game = WordGame()
        self.anim = AnimatedCrowd()
        self.game_paused = True
        self.menu_state = "main"
        self.clock = pygame.time.Clock()
        
        pygame.mixer.music.load('./audios/intro.mp3')    
        pygame.mixer.music.play(-1)
    
    def run(self):
        
        # self.game.store_words()
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
                        pygame.mixer.music.play(-1)
                    if add_word_button.draw(screen):
                        self.game.add_word() 
                    if quit_button.draw(screen):
                        pygame.quit()
                        sys.exit()
                    
                        
            # GAME LOGIC HERE
            else:   
                self.anim.update_animations()
                # The base
                pygame.draw.rect(screen, BROWN, (250, 600, 400, 20))  # Plateform
                # Poles
                pygame.draw.rect(screen, BROWN, (250, 400, 20, 200))  # Left pole
                pygame.draw.rect(screen, BROWN, (250, 380, 250, 20))  # Horizontal pole
                # Feet
                pygame.draw.rect(screen, BROWN, (320, 620, 20, 80))  # Left feet front
                pygame.draw.rect(screen, BROWN, (630, 620, 20, 80))  # Right feet front
                pygame.draw.rect(screen, BROWN, (250, 620, 20, 80))  # Left feet back
                pygame.draw.rect(screen, BROWN, (580, 620, 20, 80))  # Right feet back
                # Stairs
                for i in range(5):
                    pygame.draw.rect(screen, BROWN, (220, 620 + i * 20, 80, 10))
                
                self.anim.draw_audience()
                
                self.game.draw()         
                self.game.show_lines()
                
                # CHECK VICTORY OR DEFEAT HERE
                if self.game.life == 0:
                    pygame.time.wait(500)
                    result = self.game.show_defeat_screen() 
                    self.game_paused = True 
                    self.menu_state = "main" 
                elif set(self.game.chosen_word) == set(self.game.lettre_mot):
                    pygame.time.wait(500)
                    result = self.game.show_victory_screen() 
                    self.game_paused = True 
                    self.menu_state = "main" 
                else:
                    result = None

                if result: 
                    self.game_paused = True 
                    self.menu_state = "main" 
                elif result == False:  
                    pygame.quit()
                    sys.exit()
                
                pygame.display.flip() # To update the screen after each loop
                self.clock.tick(120)

                
            # Event Handling / Keys pressed
            for event in pygame.event.get():
                
                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_SPACE:
                #        self.game_paused = True
                
                if event.type == QUIT:
                    # self.game.is_running = False
                    pygame.quit()
                    sys.exit()
                    
                
                # Keyboard letters during game
                if event.type == KEYDOWN:
                    for letter in self.game.letters:
                        if letter == event.unicode.lower():
                            for letter2 in self.game.lettre_utilisé:
                                if event.unicode.lower() == letter2 and (len(self.game.lettre_fausse) != 6 and event.unicode.lower() != self.game.who[self.game.are]):
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
                                if len(self.game.lettre_fausse) == 6 and event.unicode.lower() == self.game.who[self.game.are]:
                                    self.game.draw()
                                    self.game.you.append(event.unicode.lower())
                                    self.game.are += 1
                                    if len(self.game.who) == len(self.game.you):
                                        pygame.mixer.music.stop()
                                        screen.blit(perso2_scaled, (0,0))
                                        scream = pygame.mixer.Sound('./audios/sound.MP3')
                                        scream.set_volume(1)
                                        scream.play()
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
                                    self.game.life -= 1
                                    print(self.game.life)
                                    # print(f"ceci est {self.game.lettre_mot}")
                                    self.game.draw()
                            else:
                                self.enter = 0
                            #print("Vous avez tapé {}".format(event.unicode))
                            #print(self.game.lettre_utilisé)
                            #print(self.game.lettre_fausse)
                            #print(self.game.lettre_mot)
                            #print(self.game.you)
                
                
                    
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
    
    
    