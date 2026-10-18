import urllib.request  # Fix for urllib.request
import pdb
import string
import re
import pickle
from collections import Counter
import math
import itertools
import pickle
import pandas as pd
import random as rnd
from wordle_solver import out_dict_ita, answer_words_ita, valid_guesses_ita


# Function to create one_word_dict
def create_one_word_dict():
    # Iterate through all possible Wordle outputs (243 combinations: 3^5)
    possible_outputs = list(itertools.product([0, 1, 2], repeat=5))

    one_word_dict = {}

    for guessed_word in valid_guesses_ita:  # Limit to the first 100 words for testing
        outputs_with_one_word = []
        for wordle_output in possible_outputs:
            # Check if the output exists for the guessed word
            if wordle_output in out_dict_ita[guessed_word]:
                possible_words = out_dict_ita[guessed_word][wordle_output]
                if len(possible_words) == 1 and possible_words[0] in answer_words_ita and possible_words[0] != guessed_word:
                    outputs_with_one_word.append((wordle_output, possible_words[0]))

        if outputs_with_one_word:
            one_word_dict[guessed_word] = outputs_with_one_word

    # Save the one_word_dict to a file
    with open('one_word_dict.pkl', 'wb') as f:
        pickle.dump(one_word_dict, f)

    print("one_word_dict has been saved to 'one_word_dict.pkl'.")



# Function to play the Wordle game
def wordle_game():
    # Load the precomputed one_word_dict
    with open('one_word_dict.pkl', 'rb') as f:
        one_word_dict = pickle.load(f)
    
    x = rnd.randint(0, len(one_word_dict) - 1)
    #pdb.set_trace()
    print("Welcome to the Wordle Solver Game!")
    guessed_word = list(one_word_dict.keys())[x]
    
    y = rnd.randint(0, len(one_word_dict[guessed_word]) - 1)

    print(guessed_word , one_word_dict[guessed_word][y][0])
    
    
    wordle_output = input("Enter the Wordle output ").strip()

    if wordle_output == one_word_dict[guessed_word][y][1]:
        print("Congratulations! You've guessed the correct word!")
    
    else: 
        print("Sorry, that's not correct. The correct word was:", one_word_dict[guessed_word][y][1])
    # Main entry point
if __name__ == "__main__":
    # Uncomment the following line if you want to regenerate one_word_dict
    # create_one_word_dict()

    # Start the game
    wordle_game()

