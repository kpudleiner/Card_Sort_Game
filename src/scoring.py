from base_db import BaseDB
import numpy as np
import pandas as pd


class ScoringDeck:
    """
    """

    def __init__(self, cards: str , p1: str, p2:str ) -> dict :

        DECK_SIZE = 52

        self.cards = cards
        self.cards_left = DECK_SIZE

        self.p1 = p1
        self.p2 = p2

        self.p1_tricks = 0
        self.p2_tricks = 0
        self.p1_cards = 0
        self.p2_cards = 0

        self.scored = False
        self.db = BaseDB(path='deck_scoring.sqlite', create=True)


    def __repr__(self):
        return f"DeckStack(cards={self.cards})"

    def score_deck(self):
        patterns = [self.p1, self.p2]
        #print(patterns)
        while self.cards_left > 2:
            indices = {pattern: self.cards.find(pattern) + 3 for pattern in patterns}
            #indices = find_first_pattern(deck_str, patterns)
            #print(indices)
            indices_vals = list(indices.values())
            if indices_vals[0] == 2 and indices_vals[1] == 2:
                print('game over')
                break
            elif indices_vals[0] < indices_vals[1] and indices_vals[0] != 2:
                self.p1_tricks += 1
                self.p1_cards += indices_vals[0]
                self.cards_left = self.cards_left - indices_vals[0]
            else:
                self.p2_tricks +=1
                self.p2_cards += indices_vals[1]
                self.cards_left = self.cards_left - indices_vals[1]

            #print(self.p1_tricks, self.p2_tricks)
            #print(self.p1_cards, self.p2_cards)

            if indices_vals[0] == 2: cards_gone = indices_vals[1]
            elif indices_vals[1] == 2: cards_gone = indices_vals[0]
            else: cards_gone = min(indices.values())
            self.cards = self.cards[cards_gone:]
            #print(self.cards)
            #print(self.cards_left)

        final_counts = {'p1_tricks': self.p1_tricks, 
                        'p2_tricks': self.p2_tricks,
                        'p1_cards': self.p1_cards,
                        'p2_cards': self.p2_cards
                        }
        self.scored = True
        return final_counts
    
    def save_scores(self):
        if self.scored == False:
            raise PermissionError("You must run .score_deck() before you can save the results using .save_scores()")
        sql = f"""
        INSERT INTO deck_scores (
            deck, p1, p2, p1_tricks, p2_tricks, p1_cards, p2_cards
        ) VALUES (
            '{self.cards}', '{self.p1}', '{self.p2}', {self.p1_tricks}, {self.p2_tricks}, {self.p1_cards}, {self.p2_cards}
        );
        """
        self.db.run_action(sql, commit=True)
        
    
deck = np.load(f'../Decks/DeckStack_0_10000.npy')[0]
#print(deck)

deck_str = ''.join(map(str, deck))
print(deck_str)

test = ScoringDeck(deck_str, '111', '001')
final_counts = test.score_deck()
print(final_counts)
test.save_scores()


db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite', create=True)
sql = """
SELECT * FROM deck_scores
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