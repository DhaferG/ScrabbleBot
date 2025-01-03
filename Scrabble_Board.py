class ScrabbleBoard:
    def __init__(self):
        """
        Initialise un plateau de Scrabble 15x15 avec des bonus prédéfinis.
        """
        # Plateau 15x15, chaque case contient soit une lettre, soit un bonus
        self.board = [['' for _ in range(15)] for _ in range(15)]

        # Bonus : (x, y) -> "bonus_type"
        # "DL": Double Lettre, "TL": Triple Lettre, "DW": Double Mot, "TW": Triple Mot
        self.bonus = {
    # Triple Word Score (TW)
    (0, 0): "TW", (0, 7): "TW", (0, 14): "TW",
    (7, 0): "TW", (7, 14): "TW",
    (14, 0): "TW", (14, 7): "TW", (14, 14): "TW",

    # Double Word Score (DW)
    (1, 1): "DW", (2, 2): "DW", (3, 3): "DW", (4, 4): "DW",
    (10, 10): "DW", (11, 11): "DW", (12, 12): "DW", (13, 13): "DW",
    (1, 13): "DW", (2, 12): "DW", (3, 11): "DW", (4, 10): "DW",
    (10, 4): "DW", (11, 3): "DW", (12, 2): "DW", (13, 1): "DW",
    (7, 7): "DW",  # Case centrale (★)

    # Triple Letter Score (TL)
    (1, 5): "TL", (1, 9): "TL",
    (5, 1): "TL", (5, 5): "TL", (5, 9): "TL", (5, 13): "TL",
    (9, 1): "TL", (9, 5): "TL", (9, 9): "TL", (9, 13): "TL",
    (13, 5): "TL", (13, 9): "TL",

    # Double Letter Score (DL)
    (0, 3): "DL", (0, 11): "DL",
    (2, 6): "DL", (2, 8): "DL",
    (3, 0): "DL", (3, 7): "DL", (3, 14): "DL",
    (6, 2): "DL", (6, 6): "DL", (6, 8): "DL", (6, 12): "DL",
    (7, 3): "DL", (7, 11): "DL",
    (8, 2): "DL", (8, 6): "DL", (8, 8): "DL", (8, 12): "DL",
    (11, 0): "DL", (11, 7): "DL", (11, 14): "DL",
    (12, 6): "DL", (12, 8): "DL",
    (14, 3): "DL", (14, 11): "DL",
}

    def place_letter(self, x, y, letter):
        """
        Place une lettre à la position (x, y). Si la case est déjà occupée, 
        vérifie si la lettre est identique. Sinon, soulève une exception.
        """
        if self.board[x][y] == '' or self.board[x][y] == letter:
            self.board[x][y] = letter
        elif self.board[x][y] == letter:
            # La lettre correspond déjà à celle placée, pas besoin de changer.
            pass
        else:
            # La case est occupée par une lettre différente, conflit détecté.
            raise ValueError(f"Conflit détecté : La case ({x}, {y}) contient déjà '{self.board[x][y]}', "
                            f"impossible d'y placer '{letter}'.")


    def is_letter_on_board(self, letter):
        """Vérifie si une lettre est présente sur le plateau."""
        for row in self.board:
            if letter in row:
                return True
        return False
    def get_bonus(self, x, y):
        """
        Retourne le type de bonus pour une case donnée (ou None si pas de bonus).
        """
        return self.bonus.get((x, y))

    def calculate_word_score(self, word, start_x, start_y, direction, letter_scores):
        """
        Calcule le score d'un mot placé à partir d'une position de départ,
        dans une direction donnée (horizontale ou verticale).
        """
        score = 0
        word_multiplier = 1

        dx, dy = (1, 0) if direction == "vertical" else (0, 1)

        for i, letter in enumerate(word):
            x, y = start_x + i * dx, start_y + i * dy
            if not (0 <= x < 15 and 0 <= y < 15):
                raise ValueError(f"Le mot dépasse les limites du plateau à la position ({x}, {y}).")

            letter_score = letter_scores[letter.lower()]
            bonus = self.get_bonus(x, y)

            if bonus == "DL":
                letter_score *= 2
            elif bonus == "TL":
                letter_score *= 3
            elif bonus == "DW":
                word_multiplier *= 2
            elif bonus == "TW":
                word_multiplier *= 3

            score += letter_score

        return score * word_multiplier

    def display(self):
        """
        Affiche le plateau de manière lisible.
        """
        for row in self.board:
            print(' '.join(cell if cell else '.' for cell in row))
    def get_all_words_on_board(self):
        """
        Retourne tous les mots présents sur le plateau avec leur direction et position.

        :param board: Instance de ScrabbleBoard.
        :return: Liste de tuples (mot, direction, position).
        """
        words = []

        # Parcourir les lignes (mots horizontaux)
        for row_idx, row in enumerate(self.board):
            current_word = ""
            start_col = None
            for col_idx, cell in enumerate(row):
                if cell != '':  # Une lettre est présente
                    if current_word == "":  # Début d'un nouveau mot
                        start_col = col_idx
                    current_word += cell
                else:  # Une case vide, fin du mot
                    if len(current_word) > 1:  # Ajouter les mots valides (au moins 2 lettres)
                        words.append((current_word, "horizontal", (row_idx, start_col)))
                    current_word = ""
                    start_col = None
            if len(current_word) > 1:  # Vérifier le dernier mot de la ligne
                words.append((current_word, "horizontal", (row_idx, start_col)))

        # Parcourir les colonnes (mots verticaux)
        for col_idx in range(15):  # Le plateau Scrabble est de taille 15x15
            current_word = ""
            start_row = None
            for row_idx in range(15):
                cell = self.board[row_idx][col_idx]
                if cell != '':  # Une lettre est présente
                    if current_word == "":  # Début d'un nouveau mot
                        start_row = row_idx
                    current_word += cell
                else:  # Une case vide, fin du mot
                    if len(current_word) > 1:  # Ajouter les mots valides (au moins 2 lettres)
                        words.append((current_word, "vertical", (start_row, col_idx)))
                    current_word = ""
                    start_row = None
            if len(current_word) > 1:  # Vérifier le dernier mot de la colonne
                words.append((current_word, "vertical", (start_row, col_idx)))

        return words
    def place_word(self, word, start_x, start_y, direction):
        """
        Place un mot sur le plateau en utilisant `place_letter`.
        
        Args:
            word (str): Le mot à placer.
            start_x (int): Ligne de départ (0-14).
            start_y (int): Colonne de départ (0-14).
            direction (str): 'horizontal' ou 'vertical'.
        
        Raises:
            ValueError: Si le mot dépasse les limites ou entre en conflit avec des lettres existantes.
        """
        dx, dy = (0, 1) if direction == "horizontal" else (1, 0)

        for i, letter in enumerate(word):
            x, y = start_x + i * dx, start_y + i * dy

            # Vérification des limites du plateau
            if not (0 <= x < 15 and 0 <= y < 15):
                raise ValueError(f"Le mot dépasse les limites du plateau à la position ({x}, {y}).")

            # Vérification des conflits avec les lettres existantes
            if self.board[x][y] not in ('', letter):
                raise ValueError(f"Conflit de lettre à la position ({x}, {y}).")

        # Si tout va bien, place le mot
        for i, letter in enumerate(word):
            x, y = start_x + i * dx, start_y + i * dy
            self.place_letter(x, y, letter)
    def is_letter_on_board(self, letter):
        """
        Vérifie si une lettre spécifique est présente sur le plateau.
        
        Args:
            letter (str): La lettre à rechercher.
            
        Returns:
            bool: True si la lettre est présente sur le plateau, False sinon.
        """
        for row in self.board:
            if letter in row:
                return True
        return False