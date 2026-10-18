# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] toc=true
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#English" data-toc-modified-id="English-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>English</a></span></li><li><span><a href="#Italiano" data-toc-modified-id="Italiano-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Italiano</a></span></li><li><span><a href="#Machiavelli" data-toc-modified-id="Machiavelli-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Machiavelli</a></span></li></ul></div>

# %%
import urllib.request  # Fix for urllib.request
import pdb
import string
import re
from collections import Counter
import math
import itertools
import pickle
import pandas as pd

# %% [markdown]
# # Italiano

# %%
with open('guesslist_ita.txt', newline='\n') as f:
    answer_words_ita = []
    for line in f:
        answer_words_ita.append(line[:5])

with open('wordlist_ita.txt', newline='\n') as f:
    valid_guesses_ita = []
    for line in f:
        valid_guesses_ita.append(line[:5])

with open('entropy_results_ita.pkl', 'rb') as f:
    word_dict_ita, out_dict_ita, prob_dict_ita, entropy_dict_ita = pickle.load(f)

entropy_df_ita = pd.DataFrame(word_dict_ita.items(), columns=['word', 'entropy'])


# %%
def score_guess(word_try, word_guess):
    res = [0,0,0,0,0]
    try_count = Counter(word_try)
    guess_count = Counter(word_guess)
    for idx in range(len(word_try)):
        if word_try[idx] not in word_guess:
            res[idx] = 0
            
        if word_try[idx] in word_guess and word_try[idx] != word_guess[idx]:
            res[idx] = 1
            
        if word_try[idx] == word_guess[idx]:
            res[idx] =2
            
    for letter in try_count.keys():
        if try_count[letter] == 2 and guess_count[letter] == 1:
            dup_idx = [index for index, value in enumerate(word_try) if value == letter]
            #pdb.set_trace()
            if res[dup_idx[0]] == 2 and res[dup_idx[-1]] == 1:
                res[dup_idx[-1]] = 0
            if res[dup_idx[0]] == 1 and res[dup_idx[-1]] == 2:
                res[dup_idx[0]] = 0
            if res[dup_idx[0]] == 1 and res[dup_idx[-1]] == 1:
                res[dup_idx[-1]] = 0

        if try_count[letter] == 3 and guess_count[letter] == 1:
            dup_idx = [index for index, value in enumerate(word_try) if value == letter]
            outcome = [res[i] for i in dup_idx]
            if 2 in outcome:
                for i in dup_idx:
                    if res[i] == 1:
                        res[i] = 0
        
        if try_count[letter] == 3 and guess_count[letter] == 2:
            dup_idx = [index for index, value in enumerate(word_try) if value == letter]
            outcome = [res[i] for i in dup_idx]
            if Counter(outcome)[2] == 0:
                res[dup_idx[-1]] = 0
            
            if Counter(outcome)[2] == 1:
                if res[dup_idx[-1]] == 1:
                    res[dup_idx[-1]] = 0
                else:
                    res[dup_idx[-2]] = 0
                    
            if Counter(outcome)[2] == 2:
                for i in dup_idx:
                    if res[i] == 1:
                        res[i] = 0

    return tuple(res)
        
        

# %%
def calculate_entropy(word_try, word_list):
    word_dict = {}
    out_dict = {}
    entropy_dict = {}
    prob_dict = {}
    for word in word_try:
        for w in word_list:
            # simulate the feedback pattern (0/1/2 per letter) 'word' would get if 'w' were the true answer
            out = score_guess(word, w)
            if word not in out_dict.keys():
                out_dict[word] = {out: [w]}
            else:
                if out not in out_dict[word].keys():
                    out_dict[word][out] = [w]
                else:
                    # group answer-words by the feedback pattern they'd produce
                    out_dict[word][out].append(w)

        for p in out_dict[word].keys():
            if word not in prob_dict.keys():
                # probability of pattern p = fraction of answer words that produce it
                prob_dict[word] = {p: (len(out_dict[word][p]) / len(word_list))}
                # entropy contribution of pattern p: p * log2(1/p)
                entropy_dict[word] = {p: (len(out_dict[word][p]) / len(word_list)) * math.log2(len(word_list) / len(out_dict[word][p]))}
            else:
                prob_dict[word][p] = (len(out_dict[word][p]) / len(word_list))
                entropy_dict[word][p] = (len(out_dict[word][p]) / len(word_list)) * math.log2(len(word_list) / len(out_dict[word][p]))

            # total expected information gain for guessing 'word' = sum of entropy over all possible patterns
            word_dict[word] = sum(entropy_dict[word].values())

    return word_dict, out_dict, prob_dict, entropy_dict


# %%
'''
word_dict_ita, out_dict_ita, prob_dict_ita, entropy_dict_ita = calculate_entropy(valid_guesses_ita, valid_guesses_ita)

with open('entropy_results_ita.pkl', 'wb') as f:
    pickle.dump((word_dict_ita, out_dict_ita, prob_dict_ita, entropy_dict_ita), f)
'''


# %%
def wordle_solver(word_list, prev_word_list=None, i=0, out_dict=out_dict_ita, prob_dict=prob_dict_ita, entropy_dict=entropy_dict_ita, entropy_df=entropy_df_ita, valid_guesses=valid_guesses_ita):
    i += 1
    if i == 1:
        print('The best words are:')
        print(entropy_df.sort_values(by='entropy', ascending=False).head())

    else:
        word_dict, out_dict, prob_dict, entropy_dict = calculate_entropy(valid_guesses, word_list)

        ent_df = pd.DataFrame(word_dict.items(), columns=['word', 'entropy'])
        ent_df['guess'] = [1 if x in word_list else 0 for x in list(ent_df['word'])]
        print('The best words are:')
        print(ent_df.sort_values(['entropy', 'guess'], ascending=[False, False]).head())

    print('Please, select new word:')
    new_word = input()
    print('Wordle output')
    new_wordle_outcome = input()
    wordle_outcome = tuple([int(i) for i in new_wordle_outcome])

    new_word_list = out_dict[new_word][wordle_outcome]
    final_word_list = [x for x in new_word_list if x in word_list]

    print('The probably was:', prob_dict[new_word][wordle_outcome])
    print('Entropy:', entropy_dict[new_word][wordle_outcome])
    print('There are', len(out_dict[new_word][wordle_outcome]), 'possible matches')
    if len(out_dict[new_word][wordle_outcome]) == 1:
        print('the word is:')
        print(out_dict[new_word][wordle_outcome][0])  # Add this line to print the word    
        return out_dict[new_word][wordle_outcome][0]

    if len(out_dict[new_word][wordle_outcome]) <= 15:
        print(out_dict[new_word][wordle_outcome])

    return wordle_solver(final_word_list, word_list, i, out_dict, prob_dict, entropy_dict, entropy_df, valid_guesses)


# %%
# Only execute this block if the script is run directly
if __name__ == "__main__":
    # Example code for testing or generating data
    print("This code runs only when wordle_solver.py is executed directly.")
    wordle_solver(valid_guesses_ita)
# %%

# %% [markdown] heading_collapsed=true
# # English

# %% hidden=true
# Download the English word list
url = "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
file = urllib.request.urlopen(url)

# Store the English words in a list
valid_guesses_eng = []
for line in file:
    decoded_line = line.decode("utf-8")
    valid_guesses_eng.append(decoded_line.replace('\n', ''))
    #put everything in lower letter
    valid_guesses_eng = [word.lower() for word in valid_guesses_eng]

answer_words_eng = valid_guesses_eng

# Save the English word list
with open('wordlist_eng.txt', 'w') as f:
    for word in valid_guesses_eng:
        f.write(word + '\n')

# %%

# %%
'''word_dict_eng, out_dict_eng, prob_dict_eng, entropy_dict_eng = calculate_entropy(valid_guesses_eng, answer_words_eng)

#save results
with open('entropy_results_eng.pkl', 'wb') as f:
    pickle.dump((word_dict_eng, out_dict_eng, prob_dict_eng, entropy_dict_eng), f)
'''

# %%
# Load previously computed entropy results for English to avoid recomputation
with open('entropy_results_eng.pkl', 'rb') as f:
    word_dict_eng, out_dict_eng, prob_dict_eng, entropy_dict_eng = pickle.load(f)

entropy_df_eng = pd.DataFrame(word_dict_eng.items(), columns=['word', 'entropy'])

# %%
#wordle_solver(answer_words_eng, out_dict=out_dict_eng, prob_dict=prob_dict_eng, entropy_dict=entropy_dict_eng, entropy_df=entropy_df_eng, valid_guesses=valid_guesses_eng)
