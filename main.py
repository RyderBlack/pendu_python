import re # used in def store_words() to remove '\n' in file list
import random

my_words = []
life = 7
game_state = {"chosen_word" : ""}

def store_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            

def shuffle_words():
    random.shuffle(my_words)
    # chosen_word = my_words[0]
    game_state["chosen_word"] = my_words[0]
    print(game_state['chosen_word'])
    # return game_state['chosen_word']

  
def dislay_hints():
    shuffling = shuffle_words()
    length_hint= len(shuffling)
    print("_" * length_hint)
    return shuffling
    
    
def add_word():
    added_word = input("entrez votre mot: ").lower()
       
    if added_word in my_words:
            print(f"Le mot {added_word} est déjà dans la liste, merci d'en choisir un autre.")          
    else:
        my_words.append(added_word)
        word_file = open("words.txt", "a")
        word_file.write("\n"+added_word)
        word_file.close()
        print(f"Ajout du mot {my_words[-1]} à la base de donnée.")
            
    
def menu():
    menu = """
    1. Jouer
    2. Ajouter un nouveau mot
    """
    print(menu)
    
    
def guess_the_word():
    letter = input("Guess a letter: ")
    chosen_word = game_state["chosen_word"]
    if letter in chosen_word:
        print(letter)
      
        
def main():
    while True:
        try:
            # display menu
            menu()
            # open file and store words into list
            store_words()
            
            user_choice = input("Entrez votre choix: ")
            #if choice == jouer:
            if user_choice == "1":
                #shuffle the list, grab one word and display hints for this word
                dislay_hints()
                guess_the_word()
            #if choice == add_word:
            elif user_choice == "2":    
                add_word()

            else:
                print("Merci de faire un choix entre 1 et 2.")
        
        except KeyboardInterrupt:
            print("Thank you!")

        
if __name__ == "__main__":
    main() 