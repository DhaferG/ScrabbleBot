
import dafsa
import pickle

def build_or_load_dawg(dictionary_file, save_file):
   
    try:
        # Charger le DAWG depuis un fichier sauvegard�
        with open(save_file, "rb") as f:
            dawg = pickle.load(f)
            print("DAWG charge depuis le fichier sauvegarde.")
            return dawg
    except (FileNotFoundError, EOFError):
        # Construire le DAWG � partir d'un fichier dictionnaire
        with open(dictionary_file, "r") as f:
            words = [line.strip() for line in f if line.strip()]
        dawg = dafsa.DAFSA(words)
        # Sauvegarder le DAWG pour les prochaines ex�cutions
        with open(save_file, "wb") as f:
            pickle.dump(dawg, f)
            print("DAWG construit et sauvegarde.")
        return dawg
