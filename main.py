import re

my_words = []

def print_words():
    with open ('words.txt', 'rt') as myfile:
        for myword in myfile:
            myword = re.sub('\n', '', myword)
            my_words.append(myword)
            
            if "r" in myword:
                print(myword)
            
    print(my_words)
    
    
print_words()