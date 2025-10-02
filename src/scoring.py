from scoring_methods import ScoringDeck
from base_db import BaseDB
import numpy as np

db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite')

sql = "DELETE FROM deck_scores"
db.run_action(sql, commit=True)

decks = np.load(f'../Decks/DeckStack_0_10000.npy')[:5]
#print(deck)
for deck in decks:
    deck_str = ''.join(map(str, deck))
    print(deck_str)
    
    test = ScoringDeck(deck_str)
    test.score_save_all_combos()

sql = """
SELECT * FROM player_wins
"""

print(db.run_query(sql))


# patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
# for pattern in patterns:
#     for pattern_2 in patterns:
#         if pattern != pattern_2:

#             deck_to_score = ScoringDeck(deck_str, pattern, pattern_2)
#             final_counts = deck_to_score.score_deck()

#             print(pattern, pattern_2)
#             print(final_counts)

        

###PREVIOUS

# deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
# print(deck)

# deck_str = ''.join(map(str, deck))
# print(deck_str)

# def find_first_pattern(deck, patterns):
#     indices = {pattern: deck.find(pattern) + 3 for pattern in patterns}
#     if 2 in indices.values():
#         #end_game(indices)
#         print('one pattern not found')
#         indices = {k: (None if v == 2 else v) for k, v in indices.items()}
#     else:
#         indices = {pattern: deck.find(pattern) for pattern in patterns}
#     return indices

# patterns = ['111', '001']

# p1_tricks = 0
# p2_tricks = 0
# p1_cards = 0
# p2_cards = 0

# cards_left = len(deck_str)
# while len(deck_str) > 2:
#     indices = find_first_pattern(deck_str, patterns)
#     print(indices)
#     indices_vals = list(indices.values())
#     if indices_vals[0] < indices_vals[1]:
#         p1_tricks += 1
#         p1_cards += indices_vals[0]
#         cards_left = cards_left - p1_cards
#     else:
#         p2_tricks +=1
#         p2_cards += indices_vals[1]
#         cards_left = cards_left - p2_cards
#     print(p1_tricks, p2_tricks)
#     print(p1_cards, p2_cards)
#     deck_str = deck_str[min(indices.values()):]
#     print(deck_str)


# cards_left = 52
# while cards_left > 2:
#     indicies = find_first_pattern(deck, patterns)