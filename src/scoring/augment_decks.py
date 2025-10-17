from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods import score_all_unscored_decks
from src.figures.create_figures import update_figures


import pandas as pd
import os

def augment_decks(num_decks):
    num_decks = num_decks

    print(f'Creating {num_decks} new decks.')

    if num_decks < 10000:
        decks_npy = DeckStackNpy(num_decks)
        decks_npy.save_decks()
    else:
        num_10000 = num_decks//10000
        print(num_10000)
        remaining_decks = num_decks % 10000
        print(remaining_decks)
        for i in range(num_10000):
            decks_npy = DeckStackNpy(10000)
            decks_npy.save_decks()
        if remaining_decks != 0:
            decks_npy = DeckStackNpy(remaining_decks)
            decks_npy.save_decks()

    print(f'Scoring {num_decks} new decks.')

    score_all_unscored_decks()

    print('Updating Figures')

    update_figures()

    print('Updates results are located in src/scoring/player_wins.csv\nUpdated figures are located in the Figures folder.')