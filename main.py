import re
import string

my_words = []

def print_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            
            if "r" in myword:
                print(myword)
            
    print(my_words)

current_index = 0

def get_letter():
    global current_index
    letters = list(string.ascii_lowercase)
    if current_index < len(letters):
        letter = letters[current_index]
        current_index += 1
        return letter
    return None   
        
        
if __name__ == "__main__":
    # print_words()
    get_letter()