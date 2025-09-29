from base_db import BaseDB
import numpy as np

# db_path = 'deck_scoring.db'
# db = BaseDB(path=db_path, create=True)

# sql = """
# CREATE TABLE IF NOT EXISTS deck_scores (
#     deck TEXT,
#     p1 TEXT,
#     p2 TEXT,
#     p1_tricks INTEGER,
#     p2_tricks INTEGER,
#     p1_cards INTEGER,
#     p2_cards INTEGER
#     PRIMARY KEY(deck, p1, p2)
# );
# """
# db.run_action(sql, commit=True)

# sql = """
# CREATE TABLE IF NOT EXISTS player_wins (
#     p1 TEXT,
#     p2 TEXT,
#     p1_wins_tricks INTEGER,
#     p2_wins_tricks INTEGER,
#     p1_wins_cards INTEGER,
#     p2_wins_cards INTEGER,
#     draws_tricks INTEGER,
#     draws_tricks INTEGER
#     PRIMARY KEY(p1, p2)
# );
# """

#db.run_action(sql, commit=True)
 

deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
print(deck)

def find_first_pattern(deck, patterns):
    indices = {}
    for pattern in patterns:
        for i in range(len(deck) - 2):
            if np.array_equal(deck[i:i+3], pattern):
                indices[''.join(map(str, pattern))] = i+3
                break
        else:
            indices[''.join(map(str, pattern))] = None  # Not found
    return indices

patterns = [[1, 1, 1], [0, 0, 1]]

indicies = find_first_pattern(deck, patterns)
print(indicies)

decks = np.load(f'../Decks/DeckStack_0_10000.npy')

