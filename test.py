import urllib.request  # Fix for urllib.request
from wordle_solver import *


"""if "tiare" in answer_words_ita:
    print('"micca" is in valid_guesses_ita.')
else:
    print('"micca" is NOT in valid_guesses_ita.')
"""
x= ['me', 'mi', 'ma', 'mo', 'mu']

d = {}
for i in range(len(x)):
    if i == 4 or i * 2 == 2:
        d[x[i]] = 1
        
print(d)