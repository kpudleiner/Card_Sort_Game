from base_db import BaseDB
import numpy as np
import pandas as pd


class ScoringDeck:
    """
    """

    def __init__(self, cards: str) -> dict :

        self.DECK_SIZE = 52
        self.original_deck = cards

        self.scored = False
        self.db = BaseDB(path='deck_scoring.sqlite', create=True)

    def __repr__(self):
        return f"DeckStack(cards={self.cards})"

    def score_deck(self, p1:str, p2:str) -> dict:
        patterns = [p1, p2]

        cards = self.original_deck
        cards_left = self.DECK_SIZE

        p1_tricks = 0
        p2_tricks = 0
        p1_cards = 0
        p2_cards = 0

        while cards_left > 2:
            indices = {pattern: cards.find(pattern) + 3 for pattern in patterns}
            indices_vals = list(indices.values())
            if indices_vals[0] == 2 and indices_vals[1] == 2:
                #print('game over')
                break
            elif indices_vals[0] < indices_vals[1] and indices_vals[0] != 2:
                p1_tricks += 1
                p1_cards += indices_vals[0]
                cards_left = cards_left - indices_vals[0]
            else:
                p2_tricks +=1
                p2_cards += indices_vals[1]
                cards_left = cards_left - indices_vals[1]

            if indices_vals[0] == 2: cards_gone = indices_vals[1]
            elif indices_vals[1] == 2: cards_gone = indices_vals[0]
            else: cards_gone = min(indices.values())
            cards = cards[cards_gone:]

        final_counts = {'p1': p1,
                        'p2': p2,
                        'p1_tricks': p1_tricks, 
                        'p2_tricks': p2_tricks,
                        'p1_cards': p1_cards,
                        'p2_cards': p2_cards
                        }
        self.scored = True
        return final_counts
    
    def save_deck_score(self, final_counts: dict):
        if self.scored == False:
            raise PermissionError("You must run .score_deck() before you can save the results using .save_scores()")
        
        p1 = final_counts['p1']
        p2 = final_counts['p2']
        p1_tricks = final_counts['p1_tricks']
        p2_tricks = final_counts['p2_tricks']
        p1_cards = final_counts['p1_cards']
        p2_cards = final_counts['p2_cards']
        
        sql = f"""
        INSERT INTO deck_scores (
            deck, p1, p2, p1_tricks, p2_tricks, p1_cards, p2_cards
        ) VALUES (
            '{self.original_deck}', '{p1}', '{p2}', {p1_tricks}, {p2_tricks}, {p1_cards}, {p2_cards}
        );
        """
        self.db.run_action(sql, commit=True)

    def increment_player_wins(self, final_counts:dict):
        p1 = final_counts['p1']
        p2 = final_counts['p2']
        p1_tricks = final_counts['p1_tricks']
        p2_tricks = final_counts['p2_tricks']
        p1_cards = final_counts['p1_cards']
        p2_cards = final_counts['p2_cards']
        print(final_counts)

        sql =  """
        SELECT p1, p2, p1_wins_tricks, p2_wins_tricks, p1_wins_cards, p2_wins_cards, draws_tricks, draws_cards
        FROM player_wins
        WHERE p1 = ? AND p2 = ?
        """
        result = self.db.run_query(sql, params=(p1, p2))
    
        params = result.iloc[0]
        print(params)

        p1_wins_tricks = params['p1_wins_tricks']
        p2_wins_tricks = params['p2_wins_tricks']
        p1_wins_cards = params['p1_wins_cards']
        p2_wins_cards = params['p2_wins_cards']
        draws_tricks = params['draws_tricks']
        draws_cards = params['draws_cards']

        if p1_tricks > p2_tricks:
            p1_wins_tricks += 1
            print('p1 win', p1_wins_tricks)
        elif p2_tricks > p1_tricks:
            p2_wins_tricks += 1
            print('p2 win', p2_wins_tricks)
        else:
            draws_tricks += 1
            print('tie', draws_tricks)

        if p1_cards > p2_cards:
            p1_wins_cards += 1
        elif p2_cards > p1_cards:
            p2_wins_cards += 1
        else:
            draws_cards += 1

        print('new params:', p1, p2, p1_wins_cards, p2_wins_cards, p1_wins_tricks, p2_wins_tricks, draws_cards, draws_tricks)

        sql = f"""
        UPDATE player_wins
        SET p1_wins_tricks = {p1_wins_tricks}, p2_wins_tricks = {p2_wins_tricks}, p1_wins_cards = {p1_wins_cards}, p2_wins_cards = {p2_wins_cards}, draws_tricks = {draws_tricks}, draws_cards = {draws_cards}
        WHERE p1 = ? AND p2 = ?
        """
        params = (p1, p2)
        self.db.run_action(sql, params=params, commit=True)

    def score_save_all_combos(self):
        patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
        for pattern in patterns:
            for pattern_2 in patterns:
                if pattern != pattern_2:

                    final_counts = self.score_deck(pattern, pattern_2)
                    self.save_deck_score(final_counts)
                    self.increment_player_wins(final_counts)