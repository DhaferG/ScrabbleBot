from Scrabble_Board import ScrabbleBoard,SCORE
from Tile import Tile
from algoglouton import find_best_word
from algoglouton import is_adjacent_word_in_same_direction
from sauvegarde import build_or_load_dawg


class ScrabbleGame:
    def __init__(self, dictionary_file, save_file, ai_vs_ai=False):
        # Initialisation des composants principaux
        self.board = ScrabbleBoard()
        self.ai_vs_ai= ai_vs_ai
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
        if ai_vs_ai:
            self.ai_tiles2 =  self.tile_manager.random_letters_in_tile(7)
        else:
            self.human_tiles = self.tile_manager.random_letters_in_tile(7)
        self.ai_tiles = self.tile_manager.random_letters_in_tile(7)
        self.game_over = False
    def __str__(self):
        """Return a string representation of the board, suitable for human viewing."""

        board_colors = {
            "DL": (106, 30),
            "TL": (44, 30),
            "DW": (101, 30),
            "TW": (41, 30),
            "SL": (47, 30),
            "STAR": (101, 30)
        }

        rows = []
        for row in range(0, 15):
            cols = []
            for col in range(0, 15):
                sq = self.board.board[row][col] if self.board.board[row][col]!=' ' else ' '
                try:
                    bg, fg = board_colors.get(SCORE[(row,col)])
                except KeyError:
                    bg,fg= board_colors.get("SL")
                if sq.islower():
                    bg, fg = (43, 30)
                sq_display = f"{sq:^3}"
                sq = u"\u001b[%d;%dm %s \u001b[0m" % (bg, fg, sq_display)
                cols.append(sq)
            rows.append("".join(cols))
        return "\n".join(rows)

    def validate_word(self, word):
        """Vérifie si un mot est valide."""
        if not self.is_valid_word(word, self.human_tiles):
            return False, "Vous n'avez pas les lettres nécessaires."
        if not self.dawg.lookup(word.lower()):
            return False, "Le mot n'existe pas dans le dictionnaire."
        return True, ""

    def is_valid_word(self, word, tiles):
        """bat
        Vérifie si un mot peut être formé avec les lettres disponibles, y compris les lettres sur le plateau et les jokers.
        :param word: Le mot proposé par le joueur.
        :param tiles: Les lettres disponibles pour le joueur, avec les jokers représentés par "".
        :return: True si le mot peut être formé, False sinon.
        """
        tiles_list = list(tiles)  # Copie des tuiles disponibles
        
        # Parcourir chaque lettre du mot proposé
        for letter in word:
            if letter in tiles_list:
                # Si la lettre est dans les tuiles du joueur, on l'utilise
                tiles_list.remove(letter)
            elif self.board.is_letter_on_board(letter):
                # Si la lettre est déjà sur le plateau, on la considère comme utilisée
                pass
            elif "" in tiles_list:
                # Si un joker est disponible, on l'utilise comme cette lettre
                tiles_list.remove("")
            else:
                # Si la lettre n'est ni dans les tuiles du joueur, ni sur le plateau, ni remplaçable par un joker
                return False
        return True
    def is_connected_to_existing_word(self, word, row, col, direction):
        """
        Vérifie si le mot proposé par le joueur est connecté à un mot déjà présent sur le plateau.

        :param word: Le mot proposé par le joueur.
        :param row: La ligne de départ du mot.
        :param col: La colonne de départ du mot.
        :param direction: La direction du mot ("horizontal" ou "vertical").
        :return: True si le mot est connecté à un mot existant, False sinon.
        """
        # Parcourir les lettres du mot et vérifier la connexion
        for i, letter in enumerate(word):
            # Calculer la position actuelle de la lettre
            current_row = row + (i if direction == "vertical" else 0)
            current_col = col + (i if direction == "horizontal" else 0)

            # Vérifier si la case actuelle contient déjà une lettre
            if self.board.board[current_row][current_col] != "":
                return True

            # Vérifier les cases adjacentes
            adjacent_cells = []
            if direction == "horizontal":
                adjacent_cells = [
                    (current_row - 1, current_col),  # Case au-dessus
                    (current_row + 1, current_col),  # Case en-dessous
                ]
            elif direction == "vertical":
                adjacent_cells = [
                    (current_row, current_col - 1),  # Case à gauche
                    (current_row, current_col + 1),  # Case à droite
                ]

            # Vérifier les lettres adjacentes
            for r, c in adjacent_cells:
                if 0 <= r < len(self.board.board) and 0 <= c < len(self.board.board[0]):
                    if self.board.board[r][c] != "":
                        return True

        return False


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

    def play_human_turn(self, i):
        """Gère le tour du joueur humain."""
        while True:
            print(f"Your tiles are {self.human_tiles}")
            word = input("Entrez un mot à placer : ").lower()
            direction = input("Entrez la direction (horizontal/vertical) : ").lower()
            row = int(input("Entrez la position (row) : "))
            col = int(input("Entrez la position (col) : "))
            valid, message = self.validate_word(word)

            # Vérification spécifique pour le premier tour
            if i == 1:
                if not self.is_first_turn_valid(word, row, col, direction):
                    print("Erreur : Le mot doit passer par la case centrale (7,7) au premier tour.")
                    row = int(input("Entrez la postition (row): "))
                    col = int(input("Entrez la postition (col): "))
            if i>1:
                if not self.is_connected_to_existing_word(word, row, col, direction):
                    print("Erreur : Le mot doit être connecté à un mot existant sur le plateau.")
                    continue
                if is_adjacent_word_in_same_direction(self.board,row,col,word,direction):
                    print("Erreur : Vous avez collé un mot à un autre.")
                    continue
            if not valid:
                print(message)
                continue

            try:
                # Placement du mot sur le plateau
                self.board.place_word(word, row, col, direction)
                # Calcul du score du mot
                score_human = self.board.calculate_word_score(word, row, col, direction, self.letter_scores)
                print(f"\nVous avez placé le mot '{word}' avec un score de {score_human} !")
                # Mise à jour des lettres du joueur
                for letter in word:
                    self.human_tiles = self.human_tiles.replace(letter, "", 1)
                # Compléter les lettres pour avoir 7 tuiles
                self.human_tiles = self.refill_tiles(self.human_tiles)
                break
            except Exception as e:
                print(f"Erreur lors du placement : {e}. Réessayez.")
        return score_human


    def play_ai_turn(self,tiles, is_first_turn = False):
        best_word, max_score, best_position, best_direction = find_best_word(
            self.board, self.dawg, tiles, self.letter_scores, is_first_turn=is_first_turn)
        if best_word:
            row, col = best_position
            self.board.place_word(best_word, row, col, best_direction)
            print(f"\nL'IA a placé le mot '{best_word}' avec un score de {max_score}.")
            for letter in best_word:
                tiles = tiles.replace(letter, "", 1)
            tiles = self.refill_tiles(tiles)
        else:
            print("\nL'IA n'a pas trouvé de mot valide à jouer.")
        return max_score

    def check_game_over(self,a,b):
        """Vérifie si le jeu est terminé."""
        if not self.tile_manager.get_remaining_tiles() and not self.ai_tiles and not self.ai_tiles2:
            self.game_over = True
            print("\nLe jeu est terminé !")
            print("Calcul des scores finaux...")
            self.calculate_final_scores(a,b)

    def calculate_final_scores(self,a,b):
        """Calcule les scores finaux."""
        human_score = sum(self.letter_scores[letter] for letter in self.human_tiles)
        ai_score = sum(self.letter_scores[letter] for letter in self.ai_tiles)
        print(f"Score final : Joueur humain : {a}, IA : {b}.")
        if a > b:
            print("Félicitations ! Vous avez gagné ! 🎉")
        elif a < b:
            print("L'IA a gagné. 😞")
        else:
            print("C'est une égalité ! Bien joué !")

    def play_human_vs_AI(self):
        """Démarre le jeu."""
        i=0
        score_human=0
        score_ia=0
        while not self.game_over:
            i+=1
            print("\n--- Tour n ",i, " ---")
            print("\n--- Tour du joueur humain ---")
            print(self)
            score_human+=self.play_human_turn(i)
            print("Vous avez un score ",score_human)
            self.check_game_over(score_human,score_ia)
            if self.game_over:
                break

            print("\n--- Tour de l'IA ---")
            print(self)
            score_ia+=self.play_ai_turn(self.ai_tiles)
            print("L'IA a un score ",score_ia)
            self.check_game_over(score_human,score_human)

        print("\nMerci d'avoir joué à Scrabble !")
    def play_AI_AI(self):
        """Simulate an AI vs. AI game."""
        round_num = 0
        score_ai1 = 0
        score_ai2 = 0

        while not self.game_over:
            round_num += 1
            print(f"\n--- Round {round_num} ---")
            
            # AI 1's turn
            print("\n--- AI Player 1's Turn ---")
            print(f"\n--- AI Player 1's Tiles {self.ai_tiles} ---")
            print(self)
            if round_num==1:
                score_ai1 += self.play_ai_turn(self.ai_tiles,True)
            else:
                score_ai1 += self.play_ai_turn(self.ai_tiles)
            print(f"AI Player 1's Score: {score_ai1}")
            self.check_game_over(score_ai1, score_ai2)
            if self.game_over:
                break

            # AI 2's turn
            print("\n--- AI Player 2's Turn ---")
            print(f"\n--- AI Player 2's Tiles {self.ai_tiles2} ---")
            score_ai2 += self.play_ai_turn(self.ai_tiles2)
            print(f"AI Player 2's Score: {score_ai2}")
            self.check_game_over(score_ai1, score_ai2)

        # Final Results
        print("\nGame Over! Final Results:")
        self.calculate_final_scores(score_ai1, score_ai2)

    def refill_tiles(self, tiles):
            """Complète les tuiles d'un joueur jusqu'à en avoir 7, si possible."""
            missing_tiles = 7 - len(tiles)
            if missing_tiles > 0:
                new_tiles = self.tile_manager.random_letters_in_tile(missing_tiles)
                tiles += new_tiles
            return tiles
    def play(self):
        if self.ai_vs_ai:
            self.play_AI_AI()
        else:
            self.play_human_vs_AI()