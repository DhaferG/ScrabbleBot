from ScrabbleDictionary.BuildDictionary import build_dawg
from sauvegarde import build_or_load_dawg
from algoglouton import find_best_word

# Fichier de dictionnaire et de sauvegarde
dictionary_file = "resources/twl06.txt"
save_file = "dawg.pkl"

# Construction ou chargement du DAWG
dawg = build_or_load_dawg(dictionary_file, save_file)

# Scores des lettres (Scrabble anglais, par exemple)
letter_scores = {
    "a": 1, "b": 3, "c": 3, "d": 2, "e": 1,
    "f": 4, "g": 2, "h": 4, "i": 1, "j": 8,
    "k": 5, "l": 1, "m": 3, "n": 1, "o": 1,
    "p": 3, "q": 10, "r": 1, "s": 1, "t": 1,
    "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
}

# Lettres disponibles pour le tour
letters = "etracep"

# Trouver le meilleur mot
best_word, max_score = find_best_word(letters, dawg, letter_scores)

print(f"Meilleur mot : {best_word} avec un score de {max_score}")