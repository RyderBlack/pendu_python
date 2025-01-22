import re # used in def store_words() to remove '\n' in file list
import random



class WordGame:
    def __init__(self):
        self.my_words = []
        self.chosen_word = ""
        self.life = 7
        self.score = 0
        
    def store_words(self):
        with open ('words.txt', 'rt') as myfile:
            for myword in myfile:
                myword = re.sub('\n', '', myword)
                self.my_words.append(myword)
            
    def add_word(self):
        added_word = input("entrez votre mot: ").lower()
        
        if added_word in self.my_words:
                print(f"Le mot {added_word} est déjà dans la liste, merci d'en choisir un autre.")          
        else:
            self.my_words.append(added_word)
            word_file = open("words.txt", "a")
            word_file.write("\n"+added_word)
            word_file.close()
            print(f"Ajout du mot {self.my_words[-1]} à la base de donnée.")
        
    def shuffle_words(self):
        random.shuffle(self.my_words)
        self.chosen_word = self.my_words[0]
        print(f"Le mot choisi est: {self.chosen_word}")
        return self.chosen_word
    
    def display_hints(self):
        length_hint = len(self.chosen_word)
        print("_" * length_hint)
        return self.chosen_word
        
    def guess_the_word(self):
        while True:
            letter = input("Devine une lettre: ")
            if letter in self.chosen_word:
                print(f"GG! la lettre {letter} est bien dans le mot à deviner!")
                self.score += 1
                print(f"Ton score est maintenant de {self.score}")
                if self.score == len(self.chosen_word):
                    print("OMG! T'as gagné la game!")
                    break
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
        while True:
            try:
                
                self.game.display_menu()
                self.game.store_words()
                
                user_choice = input("Entrez votre choix: ")
                
                if user_choice == "1":
                    self.game.shuffle_words()
                    self.game.display_hints()
                    self.game.guess_the_word()
                elif user_choice == "2":    
                    self.game.add_word()
                else:
                    print("Merci de faire un choix entre 1 et 2.")
            
            except KeyboardInterrupt:
                print("\nMerci d'avoir joué!")
                break


def main():
    game_manager = GameManager()
    game_manager.run()
        
if __name__ == "__main__":
    main() 