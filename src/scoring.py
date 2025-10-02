from scoring_methods import ScoringDeck
from base_db import BaseDB
import numpy as np

# db_path = 'deck_scoring.sqlite'
# db = BaseDB(path='deck_scoring.sqlite')

# sql = "DELETE FROM deck_scores"
# db.run_action(sql, commit=True)

# decks = np.load(f'../Decks/DeckStack_0_10000.npy')[:5]
# #print(deck)
# for deck in decks:
#     deck_str = ''.join(map(str, deck))
#     print(deck_str)

#     test = ScoringDeck(deck_str)
#     test.score_save_all_combos()

# sql = """
# SELECT * FROM player_wins
# """

# print(db.run_query(sql))

deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
deck_str = ''.join(map(str, deck))
test = ScoringDeck(deck_str)
results  = test.score_deck('001', '111')
print(results)