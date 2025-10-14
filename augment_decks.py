from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods import score_all_unscored_decks, save_player_scores
from src.scoring.base_db import BaseDB
from src.scoring.deck_scoring_db_create import reset_db
import pandas as pd

num_decks = int(input("How many new decks would you like to create and score?"))

print(f'Creating {num_decks} new decks.')

if num_decks < 10000:
    decks_npy = DeckStackNpy(num_decks)
    decks_npy.save_decks()
else:
    num_10000 = num_decks//10000
    remaining_decks = num_decks % 10000
    for i in range(num_10000):
        decks_npy = DeckStackNpy(10000)
        decks_npy.save_decks()
    decks_npy = DeckStackNpy(remaining_decks)
    decks_npy.save_decks()

print(f'Scoring {num_decks} new decks.')

db = BaseDB(path='src/scoring/deck_scoring.sqlite')
sql = """
    SELECT COUNT(*) from deck_scores;
    """
print(db.run_query(sql))

score_all_unscored_decks()

print(db.run_query(sql))

save_player_scores()

print('Updating Figures')

#update figures method

