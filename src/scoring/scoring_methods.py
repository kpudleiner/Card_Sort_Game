from base_db import BaseDB
from decorators import score_timer
import numpy as np
import pandas as pd
import os
import shutil

class ScoringDeck:
    """
    This creates a deck object and scores it with the first method.
    In this case, for each pattern combination:
        -the deck scored
        -the individual score is recorded in the 'deck_score' table of deck_scoring.sqlite
        -the player scores are updated in the 'player_score' table of deck_scoring.sqlite
    """

    def __init__(self, cards: str) -> dict :

        self.DECK_SIZE = 52
        self.original_deck = cards

        self.scored = False
        self.db = BaseDB(path='deck_scoring.sqlite', create=True)

    def __repr__(self):
        return f"DeckStack(cards={self.cards})"

    def _score_deck(self, p1:str, p2:str) -> dict:
        """
        This method scores the cards in the deck.
        It takes two patterns, 'p1' and 'p2', which are the player's choices.
        They must be a three character string combination of 1s and 0s.
        The method repeatedly finds which pattern occurs first, 
        and then removes those cards until there are none left.
        """
        patterns = [p1, p2]

        cards = self.original_deck
        cards_left = self.DECK_SIZE

        p1_tricks = 0
        p2_tricks = 0
        p1_cards = 0
        p2_cards = 0

        while cards_left > 2:
            # add three to the index so that we cut off the deck after the pattern is complete
            # note that this method returns -1 if the pattern is not found, which will now be 2
            indices = {pattern: cards.find(pattern) + 3 for pattern in patterns} 
            indices_vals = list(indices.values())

            # if neither index is found, the game is over
            if indices_vals[0] == 2 and indices_vals[1] == 2:
                break
            # if pattern one is found before pattern two, or pattern two is not found, player one wins
            # increment their tricks, increment their cards, keep track of remaining cards
            elif (indices_vals[0] < indices_vals[1] and indices_vals[0] != 2) or (indices_vals[1] == 2):
                p1_tricks += 1
                p1_cards += indices_vals[0]
                cards_left = cards_left - indices_vals[0]
            # otherwise, player 2 wins, so do the same for them
            else:
                p2_tricks +=1
                p2_cards += indices_vals[1]
                cards_left = cards_left - indices_vals[1]

            #subtrack the appropriate amount of the count
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
    
    def _save_deck_score(self, final_counts: dict):
        """
        This function saves an individual deck score into the 
        "deck_scores" table of deck_scoring.sqlite.
        It takes the results from ._score_deck() and adds them to the database.
        """
        
        #Pull out values from dictionary
        p1 = final_counts['p1']
        p2 = final_counts['p2']
        p1_tricks = final_counts['p1_tricks']
        p2_tricks = final_counts['p2_tricks']
        p1_cards = final_counts['p1_cards']
        p2_cards = final_counts['p2_cards']
        
        #Insert them into the 'deck_scores' table of the database
        sql = f"""
        INSERT INTO deck_scores (
            deck, p1, p2, p1_tricks, p2_tricks, p1_cards, p2_cards
        ) VALUES (
            '{self.original_deck}', '{p1}', '{p2}', {p1_tricks}, {p2_tricks}, {p1_cards}, {p2_cards}
        );
        """
        self.db.run_action(sql, commit=True)

        return

    def _increment_player_wins(self, final_counts:dict):
        """
        This method takes the dictionary output of _.score_deck()
        and determines who won based on cards and tricks.
        It then updates the 'player_score' table to relay that information.
        """

        #pull values from dictionary
        p1 = final_counts['p1']
        p2 = final_counts['p2']
        p1_tricks = final_counts['p1_tricks']
        p2_tricks = final_counts['p2_tricks']
        p1_cards = final_counts['p1_cards']
        p2_cards = final_counts['p2_cards']

        # find current player scores
        sql =  """
        SELECT p1, p2, p1_wins_tricks, p2_wins_tricks, p1_wins_cards, p2_wins_cards, draws_tricks, draws_cards
        FROM player_wins
        WHERE p1 = ? AND p2 = ?
        """
        result = self.db.run_query(sql, params=(p1, p2))
        params = result.iloc[0]

        p1_wins_tricks = params['p1_wins_tricks']
        p2_wins_tricks = params['p2_wins_tricks']
        p1_wins_cards = params['p1_wins_cards']
        p2_wins_cards = params['p2_wins_cards']
        draws_tricks = params['draws_tricks']
        draws_cards = params['draws_cards']

        # determine which value should be incrimented based on who won
        if p1_tricks > p2_tricks:
            p1_wins_tricks += 1
        elif p2_tricks > p1_tricks:
            p2_wins_tricks += 1
        else:
            draws_tricks += 1

        if p1_cards > p2_cards:
            p1_wins_cards += 1
        elif p2_cards > p1_cards:
            p2_wins_cards += 1
        else:
            draws_cards += 1

        # update the table accordingly
        sql = f"""
        UPDATE player_wins
        SET p1_wins_tricks = {p1_wins_tricks}, p2_wins_tricks = {p2_wins_tricks}, p1_wins_cards = {p1_wins_cards}, p2_wins_cards = {p2_wins_cards}, draws_tricks = {draws_tricks}, draws_cards = {draws_cards}
        WHERE p1 = ? AND p2 = ?
        """
        params = (p1, p2)
        self.db.run_action(sql, params=params, commit=True)

        return

    @score_timer
    def score_save_all_combos(self):
        """
        This method is the final scoring method to be called.
        It goes through all 56 possible player choice combinations,
        and scores the deck for each combination.
        It caslls the methodsv_score_decks, _save_deck_score, and _increment_player_wins.
        """

        # for each possible combination of choices (except where the players choose the same)
        # score the deck, save the results, and incriment the wins
        patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
        for pattern in patterns:
            for pattern_2 in patterns:
                if pattern != pattern_2:

                    final_counts = self._score_deck(pattern, pattern_2)
                    self._save_deck_score(final_counts)
                    self._increment_player_wins(final_counts)

class ScoringDeckPd:
    """
    This 
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
            #print('indices', indices_vals)
            if indices_vals[0] == 2 and indices_vals[1] == 2:
                #print('game over')
                break
            elif (indices_vals[0] < indices_vals[1] and indices_vals[0] != 2) or (indices_vals[1] == 2):
                p1_tricks += 1
                p1_cards += indices_vals[0]
                cards_left = cards_left - indices_vals[0]
            else:
                p2_tricks +=1
                p2_cards += indices_vals[1]
                cards_left = cards_left - indices_vals[1]
            #print('tricks:', p1_tricks, p2_tricks, 'cards:', p1_cards, p2_cards)
            #print('cards left', cards_left)
            if indices_vals[0] == 2: cards_gone = indices_vals[1]
            elif indices_vals[1] == 2: cards_gone = indices_vals[0]
            else: cards_gone = min(indices.values())
            cards = cards[cards_gone:]
            #print(cards)

        final_counts = {'deck': self.original_deck,
                        'p1': p1,
                        'p2': p2,
                        'p1_tricks': p1_tricks, 
                        'p2_tricks': p2_tricks,
                        'p1_cards': p1_cards,
                        'p2_cards': p2_cards
                        }
        self.scored = True
        return final_counts

    @score_timer
    def score_save_all_combos(self):
        df = pd.DataFrame(columns = ['deck', 'p1', 'p2','p1_tricks', 'p2_tricks', 'p1_cards', 'p2_cards'])
        patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
        for pattern in patterns:
            for pattern_2 in patterns:
                if pattern != pattern_2:
                    final_counts = self.score_deck(pattern, pattern_2)
                    df = pd.concat([df, pd.DataFrame([final_counts])], ignore_index=True)
        sql = """
        INSERT INTO deck_scores (
            deck, p1, p2, p1_tricks, p2_tricks, p1_cards, p2_cards
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.db._connect()

        for _, row in df.iterrows():
            self.db.run_action(sql, params=tuple(row), keep_open=True)

        self.db._conn.commit()
        self.db._close()

    def find_player_scores(self):
        sql = """
        SELECT * FROM player_wins_view;
        """
        return self.db.run_query(sql)
    
def score_all_unscored_decks(deck_type):
    unscored_folder = "../../Decks/Unscored"
    scored_folder = "../../Decks/Scored"

    for file_name in os.listdir(unscored_folder):
        file_path = os.path.join(unscored_folder, file_name)
        print(file_path)

        score_file(file_path, deck_type)

        destination_path = os.path.join(scored_folder, file_name)
        shutil.move(file_path, destination_path)
        print(f"Moved to: {destination_path}")

def score_file(file_path, deck_type):
    decks = np.load(file_path)
    #print(deck)
    for deck in decks[:100]:
        deck_str = ''.join(map(str, deck))
        if deck_type == 'ScoringDeck':
            scoring_deck = ScoringDeck(deck_str)
        else:
            scoring_deck = ScoringDeckPd(deck_str)
        scoring_deck.score_save_all_combos()