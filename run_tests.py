from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods_copy import score_all_unscored_decks, score_file
from src.scoring.base_db import BaseDB
from src.scoring.deck_scoring_db_create import reset_db
import pandas as pd
import os

decks_npy = DeckStackNpy(10000)
decks_npy.save_decks()

score_all_unscored_decks()


# decks_npy = DeckStackNpy(10000)
# decks_npy.save_decks()

# reset_db()

# score_file('Decks/Unscored/DeckStack_34_10000.npy')

# db = BaseDB(path='src/scoring/deck_scoring.sqlite')
# sql = """
# SELECT COUNT(*) FROM deck_scores;
# """
# print(db.run_query(sql))

# for i in range(1):
#     decks_npy = DeckStackNpy(5)
#     decks_npy.save_decks()

#reset_db()

# score_all_unscored_decks()

# db = BaseDB(path='src/scoring/deck_scoring.sqlite')
# sql = """
# SELECT COUNT(*) FROM deck_scores;
# """
# print(db.run_query(sql))
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

#reset_db()

# print(pd.read_csv('src/scoring/player_wins.csv'))

###################################################################

# def augment_decks(num_decks):
#     if num_decks < 10000:
#         decks_npy = DeckStackNpy(num_decks)
#         decks_npy.save_decks()
#     else:
#         num_10000 = num_decks//10000
#         print(num_10000)
#         remaining_decks = num_decks % 10000
#         print(remaining_decks)
#         for i in range(num_10000):
#             decks_npy = DeckStackNpy(10000)
#             decks_npy.save_decks()
#         if remaining_decks != 0:
#             decks_npy = DeckStackNpy(remaining_decks)
#             decks_npy.save_decks()

#     print(f'Scoring {num_decks} new decks.')

#     db = BaseDB(path='src/scoring/deck_scoring.sqlite')
#     sql = """
#         SELECT COUNT(*) from deck_scores;
#         """
#     print(db.run_query(sql))

#     score_all_unscored_decks()

#     print(db.run_query(sql))

#     save_player_scores()

#     print('Updating Figures')

# for i in range(20):
#     os.remove('src/scoring/deck_scoring.sqlite')
#     reset_db()
#     augment_decks(50000)
