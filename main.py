import re
import random

my_words = []
wrong_guesses = 0


def store_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            
            # if not "r" in myword:
                # print(myword)
                  
    # print(my_words) 

def shuffle_words():
    global chosen_word
    random.shuffle(my_words)
    chosen_word = my_words[0]
    
    print(chosen_word)
    return chosen_word

  
def dislay_hints():
    length_hint = len(chosen_word)
    print("_" * length_hint)
    return chosen_word
    
    
def wrong_guess():
    pass
      
        
def main():
    store_words()
    shuffle_words()
    dislay_hints()

        
if __name__ == "__main__":
    main()