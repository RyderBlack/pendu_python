import requests
from bs4 import BeautifulSoup
import time
import string

def get_words_from_page(url):
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
             
        soup = BeautifulSoup(response.text, 'html.parser')
        
        words = []
        word_elements = soup.select('ul li a')
        
        for element in word_elements:
            word = element.text.strip()
            if ' ' not in word and len(word) > 4 and word.lower():
                words.append(word)
                
        return words
    
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    

current_index = 0

def get_letter():
    global current_index
    letters = list(string.ascii_lowercase)
    if current_index < len(letters):
        letter = letters[current_index]
        current_index += 1
        return letter
    return None 

def scrape_dictionary():
    letter = get_letter()
    base_url = f"https://www.le-dictionnaire.com/repertoire/{letter}{{:02d}}.html"
    all_words = set()
    page_number = 1
    
    while True:
        url = base_url.format(page_number)
        print(f"Scraping page: {url}")
        
        words = get_words_from_page(url)
        
        if not words:
            break
            
        all_words.update(words)
        
        # Add a delay to be nice to the server
        time.sleep(1)
        page_number += 1

    return sorted(list(all_words))

def save_words_to_file(words, filename="mon_dico.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

def main():
    print("Starting dictionary scraping...")
    words = scrape_dictionary()
    print(f"Found {len(words)} unique words")
    
    save_words_to_file(words)
    print(f"Words saved to mon_dico.txt")
    
   

if __name__ == "__main__":
    main()