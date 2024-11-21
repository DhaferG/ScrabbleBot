import Scrabble_Board
from ScrabbleDictionary.BuildDictionary import build_dawg
from sauvegarde import build_or_load_dawg
from algoglouton import find_best_word,generate_possible_words , generate_possible_words_with_anchor

# Fichier de dictionnaire et de sauvegarde
dictionary_file = "resources/twl06.txt"
save_file = "dawg.pkl"

# Construction ou chargement du DAWG
dawg = build_or_load_dawg(dictionary_file, save_file)

board = Scrabble_Board.ScrabbleBoard()

# Définir les scores des lettres
letter_scores = {
    "a": 1, "b": 3, "c": 3, "d": 2, "e": 1,
    "f": 4, "g": 2, "h": 4, "i": 1, "j": 8,
    "k": 5, "l": 1, "m": 3, "n": 1, "o": 1,
    "p": 3, "q": 10, "r": 1, "s": 1, "t": 1,
    "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
}

# Placer des lettres sur le plateau
board.place_letter(7, 7, 'H')
board.place_letter(7, 8, 'E')
board.place_letter(7, 9, 'L')
board.place_letter(7, 10, 'L')
board.place_letter(7, 11, 'O')

# Afficher le plateau
board.display()

# Calculer le score du mot "HELLO"
score = board.calculate_word_score("HELLO", 7, 7, "horizontal", letter_scores)
print(f"Score du mot 'HELLO' : {score}")

# Lettres disponibles pour le tour
letters = "laefdsi"
# Trouver le meilleur mot
best_word, max_score,best_position, best_direction = find_best_word(board,dawg,letters, letter_scores)

print(f"Meilleur mot : {best_word} avec un score de {max_score} à la position {best_position} dans la direction {best_direction}")