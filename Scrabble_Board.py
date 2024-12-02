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
        Place une lettre à la position (x, y) si la case est vide ou contient la même lettre.
        """
        if self.board[x][y] == '' or self.board[x][y] == letter:
            self.board[x][y] = letter
        else:
            raise ValueError(f"La case ({x}, {y}) est déjà occupée par une autre lettre.")


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

