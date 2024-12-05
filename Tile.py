import random

class Tile:
    def __init__(self):
        self.tile_bag = self.create_tile_bag()
    
    @staticmethod
    def create_tile_bag():
        """
        Crée un sac de lettres basé sur la distribution officielle de Scrabble.
        """
        tile_distribution = {
            "a": 9, "b": 2, "c": 2, "d": 4, "e": 12,
            "f": 2, "g": 3, "h": 2, "i": 9, "j": 1,
            "k": 1, "l": 4, "m": 2, "n": 6, "o": 8,
            "p": 2, "q": 1, "r": 6, "s": 4, "t": 6,
            "u": 4, "v": 2, "w": 2, "x": 1, "y": 2,
            "z": 1, " ": 2  # Les tuiles blanches
        }
        # Générer la liste complète du sac de lettres
        return [letter for letter, count in tile_distribution.items() for _ in range(count)]
    
    def random_letters_in_tile(self, num_tiles=7):
        """
        Attribue aléatoirement des lettres à partir du sac de lettres.
        
        Args:
            num_tiles (int): Nombre de lettres à attribuer.
        
        Returns:
            str: Chaîne de lettres attribuées.
        """
        random.shuffle(self.tile_bag)
        letters = []
        for _ in range(num_tiles):
            if self.tile_bag:
                letters.append(self.tile_bag.pop())
        return "".join(letters)
    
    def get_remaining_tiles(self):
        """
        Renvoie les lettres restantes dans le sac.
        """
        return len(self.tile_bag)
    def refill_tiles(self, tiles):
        """Complète les tuiles d'un joueur jusqu'à en avoir 7, si possible."""
        missing_tiles = 7 - len(tiles)
        if missing_tiles > 0:
            new_tiles = self.tile_manager.random_letters_in_tile(missing_tiles)
            tiles += new_tiles
        return tiles
