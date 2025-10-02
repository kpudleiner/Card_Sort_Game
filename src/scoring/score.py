from src.scoring.scoring_methods import ScoringDeck, ScoringDeckPd, score_all_unscored_decks, score_file
from src.scoring.base_db import BaseDB
import numpy as np

# sql = "DELETE FROM deck_scores"
# db.run_action(sql, commit=True)

# decks = np.load(f'../Decks/DeckStack_0_10000.npy')[:5]
# #print(deck)
# for deck in decks:
#     deck_str = ''.join(map(str, deck))
#     print(deck_str)

#     test = ScoringDeck(deck_str)
#     test.score_save_all_combos()

score_all_unscored_decks('ScoringDeck')

# deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
# deck_str = ''.join(map(str, deck))
# test = ScoringDeckPd(deck_str)
# test.score_save_all_combos()

db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite')

sql = """
SELECT * FROM deck_scores
"""

print(db.run_query(sql))

sql = """
SELECT * FROM player_wins
"""

print(db.run_query(sql))

# sql = """
# SELECT * FROM player_wins_view;
# """
# print(db.run_query(sql))