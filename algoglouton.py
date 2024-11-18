def calculate_word_score(word, letter_scores):
   
    return sum(letter_scores.get(letter, 0) for letter in word)

def find_best_word(letters, dawg, letter_scores):
   
    best_word = ""
    max_score = 0

    # Parcours des mots dans le DAWG
    for length in range(1, len(letters) + 1):
         for word in generate_possible_words(letters, length):
            if dawg.lookup(word):
                score = calculate_word_score(word, letter_scores)
                if score > max_score:
                    best_word = word
                    max_score = score

    return best_word, max_score
def generate_possible_words(letters, length):
    from itertools import permutations
    return set(''.join(p) for p in permutations(letters, length))
