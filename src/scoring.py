from scoring_methods import ScoringDeck, ScoringDeckPd, score_all_unscored_decks, score_file
from base_db import BaseDB
import numpy as np

db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite')

# sql = "DELETE FROM deck_scores"
# db.run_action(sql, commit=True)

# decks = np.load(f'../Decks/DeckStack_0_10000.npy')[:5]
# #print(deck)
# for deck in decks:
#     deck_str = ''.join(map(str, deck))
#     print(deck_str)

#     test = ScoringDeck(deck_str)
#     test.score_save_all_combos()

# score_all_unscored_decks()

deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
deck_str = ''.join(map(str, deck))
test = ScoringDeckPd(deck_str)
test.score_save_all_combos()

sql = """
SELECT * FROM deck_scores
"""

print(db.run_query(sql))

# sql = """
# SELECT p1
#     , p2
#     , SUM(CASE WHEN p1_tricks > p2_tricks THEN 1 ELSE 0 END) AS p1_wins_tricks
#     , SUM(CASE WHEN p2_tricks > p1_tricks THEN 1 ELSE 0 END) AS p2_wins_tricks
#     , SUM(CASE WHEN p1_cards > p2_cards THEN 1 ELSE 0 END) AS p1_wins_cards
#     , SUM(CASE WHEN p2_cards > p1_cards THEN 1 ELSE 0 END) AS p2_wins_cards
#     , SUM(CASE WHEN p1_tricks = p2_tricks THEN 1 ELSE 0 END) AS draws_tricks
#     , SUM(CASE WHEN p1_cards = p2_cards THEN 1 ELSE 0 END) AS draws_cards
# FROM deck_scores
# GROUP BY p1, p2
# ;
# """
# print(db.run_query(sql))

# sql = """
# CREATE VIEW player_wins_view AS
# SELECT p1
#     , p2
#     , SUM(CASE WHEN p1_tricks > p2_tricks THEN 1 ELSE 0 END) AS p1_wins_tricks
#     , SUM(CASE WHEN p2_tricks > p1_tricks THEN 1 ELSE 0 END) AS p2_wins_tricks
#     , SUM(CASE WHEN p1_cards > p2_cards THEN 1 ELSE 0 END) AS p1_wins_cards
#     , SUM(CASE WHEN p2_cards > p1_cards THEN 1 ELSE 0 END) AS p2_wins_cards
#     , SUM(CASE WHEN p1_tricks = p2_tricks THEN 1 ELSE 0 END) AS draws_tricks
#     , SUM(CASE WHEN p1_cards = p2_cards THEN 1 ELSE 0 END) AS draws_cards
# FROM deck_scores
# GROUP BY p1, p2
# ;
# """
# db.run_action(sql, commit=True)


# sql = """
# SELECT * FROM player_wins_view;
# """
# print(db.run_query(sql))