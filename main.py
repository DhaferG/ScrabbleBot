from Scrabble_game import ScrabbleGame


if __name__ == "__main__":
    # Initialiser le jeu avec les fichiers requis
    game = ScrabbleGame(dictionary_file="resources/twl06.txt", save_file="dawg.pkl")
    
    # Lancer la boucle principale du jeu
    game.play()
