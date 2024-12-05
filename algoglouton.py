def find_best_word(board, dawg, rack, letter_scores):
    """
    Trouve le meilleur mot à jouer en fonction du plateau, du DAWG, et des lettres disponibles.
    
    :param board: Instance de ScrabbleBoard représentant l'état actuel du plateau.
    :param dawg: DAWG contenant les mots valides.
    :param rack: Liste des lettres disponibles pour le joueur.
    :param letter_scores: Dictionnaire des scores des lettres.
    :return: Tuple (mot, score, position, direction) représentant le meilleur mot trouvé.
    """
    best_word = None
    best_score = 0
    best_position = None
    best_direction = None

    # Identifier toutes les cases avec des lettres comme points d'ancrage
    anchor_points = [(x, y) for x in range(15) for y in range(15) if board.board[x][y] != '']
    # Explorer tous les mots possibles
    if anchor_points ==[] :
        for direction in ["horizontal", "vertical"]:
            for word in generate_possible_words(dawg, rack):
                for x in range(15):
                        for y in range(15):
                            if can_place_word(board, word, x, y, direction):
                                # Calculer le score du mot avec les bonus
                                score = board.calculate_word_score(word, x, y, direction, letter_scores)
                                # Mettre à jour le meilleur mot si le score est supérieur
                                if score > best_score:
                                    best_word = word
                                    best_score = score
                                    best_position = (x, y)
                                    best_direction = direction
    else:
        for direction in ["horizontal", "vertical"]:
            for x, y in anchor_points:
                anchor_letter = board.board[x][y].lower()  # Lettre sur la case d'ancrage
                # Générer tous les mots possibles contenant la lettre d'ancrage
                for word in generate_possible_words_with_anchor(dawg, rack, anchor_letter):
                    if anchor_letter in word:
                        # Trouver la position de l'anchor_letter dans le mot
                        anchor_index = word.index(anchor_letter)
                    
                        # Calculer la position de départ du mot
                        start_x = x - anchor_index if direction == "vertical" else x
                        start_y = y - anchor_index if direction == "horizontal" else y
                    
                        # Vérifier si le mot peut être placé
                        if can_place_word(board, word, start_x, start_y, direction):
                            # Vérification supplémentaire pour s'assurer qu'aucun mot existant ne sera collé dans la même direction
                            if not is_adjacent_word_in_same_direction(board, start_x, start_y, word, direction):
                                score = board.calculate_word_score(word, start_x, start_y, direction, letter_scores)
                            
                                # Mettre à jour le meilleur mot si le score est supérieur
                                if score > best_score:
                                    best_word = word
                                    best_score = score
                                    best_position = (start_x, start_y)
                                    best_direction = direction
            for words in board.get_all_words_on_board():
                for word in generate_possible_words_with_prefix(dawg,rack,words[0]):
                    if can_place_word(board, word, words[2][0], words[2][1], words[1]):
                        # Calculer le score du mot avec les bonus
                        score = board.calculate_word_score(word, words[2][0], words[2][1], words[1], letter_scores)
                        # Mettre à jour le meilleur mot si le score est supérieur
                        if score > best_score:
                            best_word = word
                            best_score = score
                            best_position = (words[2][0], words[2][1])
                            best_direction = words[1]


    return best_word, best_score, best_position, best_direction

def generate_possible_words(dawg, rack):
    """
    Génère tous les mots possibles en utilisant les lettres disponibles dans le rack,
    sans inclure la lettre d'ancrage.
    
    :param dawg: DAWG contenant les mots valides.
    :param rack: Liste des lettres disponibles pour le joueur.
    :param anchor_letter: Lettre d'ancrage déjà présente sur le plateau.
    :return: Générateur produisant les mots valides.
    """
    from itertools import permutations
    L=list()
    # Explorer toutes les permutations possibles du rack
    for length in range(1, len(rack) + 1):  # On ne considère que les lettres du rack
        for permutation in permutations(rack, length):
            word = ''.join(permutation)
            
            # Vérifier si le mot est valide et ne contient pas l'ancrage
            if dawg.lookup(word):
                L.append(word)
    return L

def generate_possible_words_with_anchor(dawg, rack, anchor_letter):
    """
    Génère tous les mots possibles en utilisant les lettres disponibles et une lettre d'ancrage.
    
    :param dawg: DAWG contenant les mots valides.
    :param rack: Liste des lettres disponibles pour le joueur.
    :param anchor_letter: Lettre présente sur le plateau (point d'ancrage).
    :return: Générateur de mots valides.
    """
    from itertools import permutations
    L=list()
    # Inclure la lettre d'ancrage dans toutes les combinaisons possibles
    for length in range(1, len(rack) + 2):  # +1 pour inclure la lettre d'ancrage
        for perm in permutations([i[1] for i in enumerate(rack)] + [anchor_letter.lower()], length):
            word = ''.join(perm)
            if dawg.lookup(word):
                L.append(word)
    return L
def generate_possible_words_with_prefix(dawg, rack, prefix):
    """
    Génère tous les mots possibles en ajoutant des lettres à un mot existant sur le plateau (préfixe).

    :param dawg: DAWG contenant les mots valides.
    :param rack: Liste des lettres disponibles pour le joueur.
    :param prefix: Mot existant sur le plateau (préfixe).
    :return: Liste de mots valides générés.
    """
    from itertools import permutations

    valid_words = []

    # Inclure toutes les permutations des lettres du rack, ajoutées au préfixe
    for length in range(1, len(rack) + 1):  # Générer des mots de longueur croissante
        for perm in permutations(rack, length):
            candidate = prefix + ''.join(perm)  # Ajouter le préfixe au début
            if dawg.lookup(candidate):  # Vérifier si le mot est valide dans le DAWG
                valid_words.append(candidate)

    return valid_words

def is_adjacent_word_in_same_direction(board, start_x, start_y, word, direction):
    """
    Vérifie si un mot placé collerait à un mot existant dans la même direction.
    """
    word_length = len(word)
    if direction == "horizontal":
        for i in range(word_length):
            x = start_x
            y = start_y + i
            if board.board[x][y] != ' ':
                # Vérifie si la case suivante dans la direction contient une lettre
                if (y > 0 and board.board[x][y - 1] != ' ') or (y < len(board.board[0]) - 1 and board.board[x][y + 1] != ' '):
                    return True
    elif direction == "vertical":
        for i in range(word_length):
            x = start_x + i
            y = start_y
            if board.board[x][y] != ' ':
                # Vérifie si la case suivante dans la direction contient une lettre
                if (x > 0 and board.board[x - 1][y] != ' ') or (x < len(board.board) - 1 and board.board[x + 1][y] != ' '):
                    return True
    return False

def can_place_word(board, word, start_x, start_y, direction):
    """
    Vérifie si un mot peut être placé à une position donnée sans conflit.
    
    :param board: Instance de ScrabbleBoard.
    :param word: Mot à placer.
    :param start_x: Ligne de départ.
    :param start_y: Colonne de départ.
    :param direction: Direction ("horizontal" ou "vertical").
    :return: True si le mot peut être placé, False sinon.
    """
    dx, dy = (0, 1) if direction == "horizontal" else (1, 0)

    for i, letter in enumerate(word):
        x, y = start_x + i * dx, start_y + i * dy
        if not (0 <= x < 15 and 0 <= y < 15):  # Hors des limites du plateau
            return False
        if board.board[x][y].lower() not in ('', letter.lower()):  # Conflit avec une lettre existante
            return False

    return True
