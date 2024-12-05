import Scrabble_Board
from Tile import Tile
from algoglouton import find_best_word
from sauvegarde import build_or_load_dawg


class ScrabbleGame:
    def __init__(self, dictionary_file, save_file):
        # Initialisation des composants principaux
        self.board = Scrabble_Board.ScrabbleBoard()
        self.dawg = build_or_load_dawg(dictionary_file, save_file)
        self.tile_manager = Tile()
        self.letter_scores = {
            "a": 1, "b": 3, "c": 3, "d": 2, "e": 1,
            "f": 4, "g": 2, "h": 4, "i": 1, "j": 8,
            "k": 5, "l": 1, "m": 3, "n": 1, "o": 1,
            "p": 3, "q": 10, "r": 1, "s": 1, "t": 1,
            "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10,
            " ": 0  # Les tuiles blanches ont une valeur nulle
        }
        self.human_tiles = self.tile_manager.random_letters_in_tile(7)
        self.ai_tiles = self.tile_manager.random_letters_in_tile(7)
        self.game_over = False

    def display_state(self):
        """Affiche l'état actuel du plateau et des lettres du joueur."""
        print("\nÉtat actuel du plateau :")
        self.board.display()
        print(f"Lettres du joueur : {self.human_tiles}")
        # Debug : Afficher les lettres de l'IA
        # print(f"Lettres de l'IA : {self.ai_tiles}")
    
    
    
    def validate_word(self, word):
        """Vérifie si un mot est valide."""
        if not self.is_valid_word(word, self.human_tiles):
            return False, "Vous n'avez pas les lettres nécessaires."
        if not self.dawg.lookup(word.lower()):
            return False, "Le mot n'existe pas dans le dictionnaire."
        return True, ""

    def is_valid_word(self, word, tiles):
        """Vérifie si un mot peut être formé avec les lettres disponibles, y compris les lettres sur le plateau."""
        tiles_list = list(tiles)
        
        # Parcourir chaque lettre du mot proposé
        for letter in word:
            if letter in tiles_list:
                # Si la lettre est dans les tuiles du joueur, on l'utilise
                tiles_list.remove(letter)
            elif self.board.is_letter_on_board(letter):
                # Si la lettre est déjà sur le plateau, on la considère comme utilisée
                pass
            else:
                # Si la lettre n'est ni dans les tuiles du joueur ni sur le plateau, le mot est invalide
                return False
        return True
    def is_first_turn_valid(self, word, start_row, start_col, direction):
        """
        Vérifie si le premier mot passe par la case centrale (7,7).
        
        :param word: Mot à placer.
        :param start_row: Ligne de départ.
        :param start_col: Colonne de départ.
        :param direction: Direction du mot ("horizontal" ou "vertical").
        :return: True si le mot passe par la case centrale, False sinon.
        """
        center_row, center_col = 7, 7
        if direction == "horizontal":
            return center_row == start_row and center_col in range(start_col, start_col + len(word))
        elif direction == "vertical":
            return center_col == start_col and center_row in range(start_row, start_row + len(word))
        return False


    def refill_tiles(self, tiles):
        """Complète les tuiles d'un joueur jusqu'à en avoir 7, si possible."""
        missing_tiles = 7 - len(tiles)
        if missing_tiles > 0:
            new_tiles = self.tile_manager.random_letters_in_tile(missing_tiles)
            tiles += new_tiles
        return tiles

    def play_human_turn(self,i):
        """Gère le tour du joueur humain."""
        while True:
            self.display_state()
            word = input("Entrez un mot à placer : ").lower()
            direction = input("Entrez la direction (horizontal/vertical) : ").lower()
            row = int(input("Entrez la postition (row): "))
            col = int(input("Entrez la postition (col): "))
            valid, message = self.validate_word(word)
            if i==1:
                while not self.is_first_turn_valid(word, row, col, direction):
                    print("Erreur : Le mot doit passer par la case centrale (7,7) au premier tour.")
                    row = int(input("Entrez la postition (row): "))
                    col = int(input("Entrez la postition (col): "))
                
            if not valid:
                print(message)
                continue
            try:
                self.board.place_word(word, row, col, direction)
                score_human=self.board.calculate_word_score(word,row,col,direction,self.letter_scores)
                print(f"\nVous avez placé le mot '{word}' avec un score '{score_human}!")
                for letter in word:
                    self.human_tiles = self.human_tiles.replace(letter, "", 1)
                self.human_tiles = self.refill_tiles(self.human_tiles)
                break
            except Exception as e:
                print(f"Erreur lors du placement : {e}. Réessayez.")
        return score_human

    def play_ai_turn(self):
        """Gère le tour de l'IA."""
        print(f"Lettres de l'IA : {self.ai_tiles}")
        best_word, max_score, best_position, best_direction = find_best_word(
            self.board, self.dawg, self.ai_tiles, self.letter_scores
        )
        if best_word:
            row, col = best_position
            self.board.place_word(best_word, row, col, best_direction)
            print(f"\nL'IA a placé le mot '{best_word}' avec un score de {max_score}.")
            for letter in best_word:
                self.ai_tiles = self.ai_tiles.replace(letter, "", 1)
            self.ai_tiles = self.refill_tiles(self.ai_tiles)
            return max_score
        else:
            print("\nL'IA n'a pas trouvé de mot valide à jouer.")
            return 0
        

    def check_game_over(self,human_score,ai_score):
        """Vérifie si le jeu est terminé."""
        if self.tile_manager.get_remaining_tiles()==0 and self.human_tiles=="" and self.ai_tiles=="":
            self.game_over = True
            print("\nLe jeu est terminé !")
            print("Calcul des scores finaux...")
            print(f"Score final : Joueur humain : {human_score}, IA : {ai_score}.")
            if human_score > ai_score:
                print("Félicitations ! Vous avez gagné ! 🎉")
            elif human_score < ai_score:
                print("L'IA a gagné. 😞")
            else:
                print("C'est une égalité ! Bien joué !")


    def play(self):
        """Démarre le jeu."""
        total_score_human=0
        total_score_ai=0
        i=0
        while not self.game_over:
            i+=1
            print("\n--- Tour n ",i," ---")
            print("\n--- Tour du joueur humain ---")
            score_human=self.play_human_turn(i)
            total_score_human+=score_human
            print("\nVous avez un score qui vaut ",total_score_human)
            self.check_game_over(total_score_human,total_score_ai)
            if self.game_over:
                break

            print("\n--- Tour de l'IA ---")
            score_ai=self.play_ai_turn()
            total_score_ai+=score_ai
            print("\nL'IA a un score qui vaut ",total_score_ai)
            self.check_game_over(total_score_human,total_score_ai)
        print("\nMerci d'avoir joué à Scrabble !")


