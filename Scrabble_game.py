import Scrabble_Board
from Tile import Tile
from algoglouton import find_best_word
from sauvegarde import build_or_load_dawg


class ScrabbleGame:
    def __init__(self, dictionary_file, save_file):
        # Initialiser le plateau, le sac de lettres, et le DAWG
        self.board = Scrabble_Board.ScrabbleBoard()
        self.dawg = build_or_load_dawg(dictionary_file, save_file)
        self.tile_manager = Tile()
        self.letter_scores = {
            "a": 1, "b": 3, "c": 3, "d": 2, "e": 1,
            "f": 4, "g": 2, "h": 4, "i": 1, "j": 8,
            "k": 5, "l": 1, "m": 3, "n": 1, "o": 1,
            "p": 3, "q": 10, "r": 1, "s": 1, "t": 1,
            "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
        }
        self.human_tiles = self.tile_manager.random_letters_in_tile(7)
        self.ai_tiles = self.tile_manager.random_letters_in_tile(7)

    def display_state(self):
        """Affiche l'état actuel du plateau et des lettres."""
        print("\nÉtat actuel du plateau :")
        self.board.display()
        print(f"Lettres du joueur : {self.human_tiles}")
        #print(f"Lettres de l'IA : {self.ai_tiles}")

    def validate_word(self, word):
        """Vérifie si un mot est valide."""
        if not self.is_valid_word(word, self.human_tiles):
            return False, "Vous n'avez pas les lettres nécessaires."
        if not self.dawg.lookup(word.lower()):
            return False, "Le mot n'existe pas dans le dictionnaire."
        return True, ""

    def is_valid_word(self, word, tiles):
        """Vérifie si un mot peut être formé avec les lettres disponibles."""
        tiles_list = list(tiles)
        for letter in word:
            if letter in tiles_list:
                tiles_list.remove(letter)
            else:
                return False
        return True

    def play_human_turn(self):
        """Gère le tour du joueur humain."""
        while True:
            self.display_state()
            word = input("Entrez un mot à placer : ").lower()
            direction = input("Entrez la direction (horizontal/vertical) : ").lower()
            row, col = 7, 7  # Première lettre sur l'étoile centrale
            valid, message = self.validate_word(word)
            if not valid:
                print(message)
                continue
            try:
                self.board.place_word(word, row, col, direction)
                print(f"\nVous avez placé le mot '{word}' !")
                for letter in word:
                    self.human_tiles = self.human_tiles.replace(letter, "", 1)
                break
            except Exception as e:
                print(f"Erreur lors du placement : {e}. Réessayez.")

    def play_ai_turn(self):
        """Gère le tour de l'IA."""
        best_word, max_score, best_position, best_direction = find_best_word(
            self.board, self.dawg, self.ai_tiles, self.letter_scores
        )
        if best_word:
            row, col = best_position
            self.board.place_word(best_word, row, col, best_direction)
            print(f"\nL'IA a placé le mot '{best_word}' avec un score de {max_score}.")
            for letter in best_word:
                self.ai_tiles = self.ai_tiles.replace(letter, "", 1)
        else:
            print("\nL'IA n'a pas trouvé de mot valide à jouer.")

    def play(self):
        """Démarre le jeu."""
        self.play_human_turn()
        self.play_ai_turn()
        self.display_state()
