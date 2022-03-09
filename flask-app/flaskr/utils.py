import random
import string

def generate_random_word(min_len:int = 3, max_len:int = 14) -> str:
    len_ = random.randint(min_len, max_len)

    letters = string.ascii_lowercase

    random_word = ''.join(random.choice(letters) for i in range(len_))

    return random_word

def generate_random_text(min_len:int = 3, max_len:int = 24) -> str:
    len_ = random.randint(min_len, max_len) 

    random_text = ' '.join(generate_random_word() for i in range(len_))

    return random_text
    
