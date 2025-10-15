from src.scoring.base_db import BaseDB
from src.scoring.deck_scoring_db_create import reset_db
from src.scoring.decorators import score_timer
import numpy as np
import pandas as pd
import os
import shutil

class ScoringDeckPd:
    """
    This creates a deck object and scores it with the second method.
    In this case, for each pattern combination:
        - the deck scored
        - the individual score is added to a pandas dataframe
    Once all combinations have been scored:
        - each row of the pandas dataframe is added to the 'deck_score' table of deck_scoring.sqlite
        - the player scores can be found using the 'player_score_view' of the 'deck_score' table
    """

    def __init__(self, cards: str) -> dict :

        self.DECK_SIZE = 52
        self.PATTERN_LEN = 3
        self.original_deck = cards

        self.scored = False
        self.db = BaseDB(path='src/scoring/deck_scoring.sqlite', create=True)

    def __repr__(self):
        return f"DeckStack(cards={self.cards})"

    def _score_deck(self, p1:str, p2:str) -> dict:
        """
        This method scores the cards in the deck.
        It takes two patterns, 'p1' and 'p2', which are the player's choices.
        They must be a three character string combination of 1s and 0s.
        The method repeatedly finds which pattern occurs first, 
        and then removes those cards until there are none left.
        It returns a dictionary of the deck, as well as the final card and trick counts.
        """
        patterns = [p1, p2]

        cards = self.original_deck
        cards_left = self.DECK_SIZE

        p1_tricks = 0
        p2_tricks = 0
        p1_cards = 0
        p2_cards = 0

        p1_wins_tricks = 0
        p2_wins_tricks = 0
        p1_wins_cards = 0
        p2_wins_cards = 0
        draws_tricks = 0
        draws_cards = 0

        while cards_left > 2:
            # add three to the index so that we cut off the deck after the pattern is complete
            # note that this method returns -1 if the pattern is not found, which will now be 2
            indices = {pattern: cards.find(pattern) + self.PATTERN_LEN for pattern in patterns}
            indices_vals = list(indices.values())

            # if neither index is found, the game is over
            if indices_vals[0] == self.PATTERN_LEN-1 and indices_vals[1] == self.PATTERN_LEN-1:
                break
            # if pattern one is found before pattern two, or pattern two is not found, player one wins
            # increment their tricks, increment their cards, keep track of remaining cards
            elif (indices_vals[0] < indices_vals[1] and indices_vals[0] != self.PATTERN_LEN-1) or (indices_vals[1] == self.PATTERN_LEN-1):
                p1_tricks += 1
                p1_cards += indices_vals[0]
                cards_left = cards_left - indices_vals[0]
            # otherwise, player 2 wins, so do the same for them
            else:
                p2_tricks +=1
                p2_cards += indices_vals[1]
                cards_left = cards_left - indices_vals[1]

            #subtract the appropriate amount from the count
            if indices_vals[0] == self.PATTERN_LEN-1: cards_gone = indices_vals[1]
            elif indices_vals[1] == self.PATTERN_LEN-1: cards_gone = indices_vals[0]
            else: cards_gone = min(indices.values())
            cards = cards[cards_gone:]

        if p1_tricks > p2_tricks:
            p1_wins_tricks += 1
        elif p2_tricks > p1_tricks:
            p2_wins_tricks += 1
        else:
            draws_tricks += 1

        if p1_cards > p2_cards:
            p1_wins_cards += 1
        elif p2_tricks > p1_tricks:
            p2_wins_cards += 1
        else:
            draws_cards += 1

        final_counts = {'p1': p1,
                        'p2': p2,
                        'p1_wins_tricks': p1_wins_tricks, 
                        'p2_wins_tricks': p2_wins_tricks,
                        'p1_wins_cards': p1_wins_cards,
                        'p2_wins_cards': p2_wins_cards,
                        'draws_tricks': draws_tricks,
                        'draws_cards': draws_cards
                        }
        self.scored = True

        return final_counts

    #@score_timer
    def score_save_all_combos(self):
        """
        This is the culminating method to be called in order to score a deck and save the results.
        It cycles through all possible choices for the players, calling ._score_deck() to score.
        It then adds each deck's score to a dataframe, and once all options have been scored,
        it inserts them into 'deck_scores' while keeping the database open.
        """

        df = pd.DataFrame(columns = ['p1', 'p2','p1_wins_tricks', 'p2_wins_tricks', 'p1_wins_cards', 'p2_wins_cards', 'draws_tricks', 'draws_cards'])
        patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
        for pattern in patterns:
            for pattern_2 in patterns:
                if pattern != pattern_2:
                    final_counts = self._score_deck(pattern, pattern_2)
                    df = pd.concat([df, pd.DataFrame([final_counts])], ignore_index=True)

        #results_df = df.groupby(['p1', 'p2'], as_index=False).sum()

        return df
    
def score_all_unscored_decks():
    """
    This function searches the "Unscored" folder in the Decks subdirectory.
    It takes any unscored deck, and calls the file_score method on it, 
    creating an instance of either the ScoringDeck or ScoringDeckPd class,
    and scoring it accordingly.
    """

    unscored_folder = "Decks/Unscored"
    scored_folder = "Decks/Scored"

    for file_name in os.listdir(unscored_folder):
        file_path = os.path.join(unscored_folder, file_name)
        print(file_path)

        score_file(file_path)

        destination_path = os.path.join(scored_folder, file_name)
        shutil.move(file_path, destination_path)
        print(f"Moved to: {destination_path}")

def score_file(file_path:str):
    """
    This function loads a single .npy file of multiple decks,
    and uses a for loop to call .score_save_all_combos().
    It takes a file path and deck_type as inputs (ScoringDeck)
    """

    current_results = pd.read_csv('src/scoring/player_wins_copy.csv', 
                                index_col = 0, 
                                dtype={'p1': str, 'p2': str})
    print(current_results)

    columns_to_sum = [
    'p1_wins_tricks', 'p2_wins_tricks',
    'p1_wins_cards', 'p2_wins_cards',
    'draws_tricks', 'draws_cards'
    ]

    decks = np.load(file_path)

    for deck in decks: 
        deck_str = ''.join(map(str, deck))
        scoring_deck = ScoringDeckPd(deck_str)
        new_results = scoring_deck.score_save_all_combos()
        print(new_results)

        current_results[columns_to_sum] = current_results[columns_to_sum] + new_results[columns_to_sum]
        
        print(current_results)
    
    current_results.to_csv('src/scoring/player_wins_copy.csv')
        

    

# def save_player_scores():
#     """
#     This function selects the view created in deck_scoring_db_create.
#     It is the equivalent of the 'player_wins' table,
#     but pulls directly from the 'deck_scores' instead of recording through the scoring process.
#     """

#     db = BaseDB(path='src/scoring/deck_scoring.sqlite')
#     sql = """
#     SELECT * FROM player_wins_view;
#     """
#     new_wins = db.run_query(sql)
#     #print(new_wins)

#     current_wins = pd.read_csv('src/scoring/player_wins.csv', 
#                             index_col = 0, 
#                             dtype={'p1': str, 'p2': str})
#     #print(current_wins)

#     columns_to_sum = [
#     'p1_wins_tricks', 'p2_wins_tricks',
#     'p1_wins_cards', 'p2_wins_cards',
#     'draws_tricks', 'draws_cards'
#     ]

#     # Create a new DataFrame by copying one of them (so we preserve the index and other columns)
#     combined_wins = current_wins.copy()

#     # Add the values from df2 for the specified columns
#     combined_wins[columns_to_sum] = current_wins[columns_to_sum] + new_wins[columns_to_sum]
#     #print(combined_wins)

#     combined_wins.to_csv('src/scoring/player_wins.csv')

#     reset_db()

#########################################################################
#     #@score_timer
#     def score_all_combos(self):
#         """
#         This is the culminating method to be called in order to score a deck and save the results.
#         It cycles through all possible choices for the players, calling ._score_deck() to score.
#         It then adds each deck's score to a dataframe, and once all options have been scored,
#         it inserts them into 'deck_scores' while keeping the database open.
#         """

#         df = pd.DataFrame(columns = ['deck', 'p1', 'p2','p1_tricks', 'p2_tricks', 'p1_cards', 'p2_cards'])

#         patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
#         for pattern in patterns:
#             for pattern_2 in patterns:
#                 if pattern != pattern_2:
#                     final_counts = self._score_deck(pattern, pattern_2)
#                     df = pd.concat([df, pd.DataFrame([final_counts])], ignore_index=True)
#         #print('One single deck scored:')
#         #print(df)
#         #print(len(df))

#         return df


    
# def score_all_unscored_decks():
#     """
#     This function searches the "Unscored" folder in the Decks subdirectory.
#     It takes any unscored deck, and calls the file_score method on it, 
#     creating an instance of either the ScoringDeck or ScoringDeckPd class,
#     and scoring it accordingly.
#     """

#     unscored_folder = "Decks/Unscored"
#     scored_folder = "Decks/Scored"

#     for file_name in os.listdir(unscored_folder):
#         file_path = os.path.join(unscored_folder, file_name)
#         print(file_path)

#         score_file(file_path)

#         destination_path = os.path.join(scored_folder, file_name)
#         shutil.move(file_path, destination_path)
#         print(f"Moved to: {destination_path}")

# def score_file(file_path:str):
#     """
#     This function loads a single .npy file of multiple decks,
#     and uses a for loop to call .score_save_all_combos().
#     It takes a file path and deck_type as inputs (ScoringDeck)
#     """
#     DB = BaseDB(path='src/scoring/deck_scoring.sqlite', create=True)

#     df = pd.DataFrame(columns = ['deck', 'p1', 'p2','p1_tricks', 'p2_tricks', 'p1_cards', 'p2_cards'])

#     decks = np.load(file_path)

#     i = 0
#     print(i)
#     for deck in decks: 
#         deck_str = ''.join(map(str, deck))
#         scoring_deck = ScoringDeckPd(deck_str)
#         df_new = scoring_deck.score_all_combos()
#         df = pd.concat([df, df_new], ignore_index=True)
#         i+=1
#         if i % 1000 == 0:
#             print(f'{i}/10,000')
#             print(len(df))
#         #print('new concat df:')
#         #print(df)
#         #print(len(df))

#     sql = """
#     INSERT INTO deck_scores (
#         deck, p1, p2, p1_tricks, p2_tricks, p1_cards, p2_cards
#     ) VALUES (?, ?, ?, ?, ?, ?, ?);
#     """
#     DB._connect()
#     for _, row in df.iterrows():
#         DB.run_action(sql, params=tuple(row), keep_open=True)
#     DB._conn.commit()
#     DB._close()

#     return



