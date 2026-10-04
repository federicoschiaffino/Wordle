# Wordle Solver

An entropy-based Wordle solver in Python, supporting both Italian and English word lists.

## How it works

- **`score_guess`** — simulates the feedback (green/yellow/gray) a guess would get against an answer.
- **`calculate_entropy`** — scores each candidate guess by expected information gain (Shannon entropy) across all possible answers.
- **`wordle_solver`** — interactive loop: suggests the best guess, takes your actual result, filters remaining candidates, repeats.

## Usage

```python
word_dict_ita, out_dict_ita, prob_dict_ita, entropy_dict_ita = calculate_entropy(valid_guesses_ita, answer_words_ita)
entropy_df_ita = pd.DataFrame(word_dict_ita.items(), columns=['word', 'entropy'])

wordle_solver(
    answer_words_ita,
    out_dict=out_dict_ita, prob_dict=prob_dict_ita,
    entropy_dict=entropy_dict_ita, entropy_df=entropy_df_ita,
    valid_guesses=valid_guesses_ita
)
```

Enter guesses and feedback as a 5-digit string (e.g. `02210`: 0=gray, 1=yellow, 2=green).

## Notes

Entropy results are cached to `.pkl` files to avoid recomputation. Large data files are excluded via `.gitignore`.
