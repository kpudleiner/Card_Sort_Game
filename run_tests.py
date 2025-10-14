from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods import score_all_unscored_decks, save_player_scores
from src.scoring.base_db import BaseDB
from src.scoring.deck_scoring_db_create import reset_db
import pandas as pd

# for i in range(1):
#     decks_npy = DeckStackNpy(10000)
#     decks_npy.save_decks()

# reset_db()

# score_all_unscored_decks()

db = BaseDB(path='src/scoring/deck_scoring.sqlite')
sql = """
SELECT COUNT(*) FROM deck_scores;
"""
print(db.run_query(sql))
# new_wins = db.run_query(sql)
# print(new_wins)

# current_wins = pd.read_csv('src/scoring/player_wins.csv', 
#                            index_col = 0, 
#                            dtype={'p1': str, 'p2': str})
# print(current_wins)

# columns_to_sum = [
# 'p1_wins_tricks', 'p2_wins_tricks',
# 'p1_wins_cards', 'p2_wins_cards',
# 'draws_tricks', 'draws_cards'
# ]

# # Create a new DataFrame by copying one of them (so we preserve the index and other columns)
# combined_wins = current_wins.copy()

# # Add the values from df2 for the specified columns
# combined_wins[columns_to_sum] = current_wins[columns_to_sum] + new_wins[columns_to_sum]
# print(combined_wins)

# combined_wins.to_csv('src/scoring/player_wins.csv')

# reset_db()

# print(pd.read_csv('src/scoring/player_wins.csv'))