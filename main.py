import re # used in def store_words() to remove '\n' in file list
import random

my_words = []
wrong_guesses = 0
life = 7

def store_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            

def shuffle_words():
    random.shuffle(my_words)
    chosen_word = my_words[0]
    
    print(chosen_word)
    return chosen_word

  
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
    
    
def wrong_guess():
    # life = 7
    pass
      
        
def main():
    # display menu
    menu()
    # open file and store words into list
    store_words()
    
    choice = input("Entrez votre choix: ")
    #if choice == jouer:
    if choice == "1":
        #shuffle the list, grab one word and display hints for this word
        dislay_hints()
    #if choice == add_word:
    elif choice == "2":    
        add_word()

    else:
        print("Merci de faire un choix entre 1 et 2.")
    
    

        
if __name__ == "__main__":
    main() 