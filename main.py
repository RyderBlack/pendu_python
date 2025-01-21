import re
import random

my_words = []
wrong_guesses = 0


def store_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            
            if not "r" in myword:
                print(myword)
                  
    print(my_words) 

def shuffle_words():
    pass
        
def main():
    pass
        
if __name__ == "__main__":
    store_words()