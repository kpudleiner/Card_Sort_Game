import numpy as np
import random
import os
from typing import Callable
from datetime import datetime as dt
import time
import pandas as pd

#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

def gen_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This is the modified version of the function that gets returned.
        '''
        print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        run_time = dt.now()- t0
        print(f'Ran for {run_time} sec(s)')

        self = args[0]
        seed = self.seed
        num_decks = self.num_decks

        if not os.path.exists('Deck_Stats.csv'):
            Deck_Stats = pd.DataFrame(columns=['num_decks', 
                                               'random_seed', 
                                               'gen_time', 
                                               'file_size', 
                                               'write_time', 
                                               'read_time'])
        else:
            Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically shouldn't happen
            raise ValueError(
                    f'Decks with this random seed have already been generatied. Please choose a different seed.'
                    )
        else:
            new_row = pd.DataFrame([{'num_decks': num_decks, 
                                    'random_seed': seed, 
                                    'gen_time': run_time.total_seconds(), 
                                    'file_size': None, 
                                    'write_time': None, 
                                    'read_time': None}])
            Deck_Stats = pd.concat([Deck_Stats, new_row], ignore_index = True)
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        return results
    return _wrapper

def write_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This is the modified version of the function that gets returned.
        '''
        print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        run_time = dt.now()- t0
        print(f'Ran for {run_time} sec(s)')

        self = args[0]
        seed = self.seed

        Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[Deck_Stats['random_seed'] == seed, 'write_time'] = run_time
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return results
    return _wrapper

def get_size(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        self = args[0]

        file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy'
        if os.path.exists(file_path):
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024*1024)
            print(f"Saved file: {file_path}")
            print(f"File size: {file_size_bytes} bytes ({file_size_mb:.2f} KB)")
        else:
            print(f"Warning: File {file_path} not found.")

        self = args[0]
        seed = self.seed
        Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[Deck_Stats['random_seed'] == seed, 'file_size'] = file_size_mb
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return result
    return _wrapper

#Method 1: soter integer 0s and 1s as numpy arrays
class DeckStack_npy:
    """
    A class to represent multiple shuffled decks.
    Takes the number of decks and random seed as input.
    If no random seed is specified, then find the largest existing seed and add one.
    
    """
    @gen_timer
    def __init__(self, num_decks: int, seed: int = None):

        self.num_decks = num_decks

        #Search existing decks to find next seed
        used_seeds = [int(file.split('_')[1]) for file in os.listdir('Decks')]
        if seed:
            if seed in used_seeds:
                raise ValueError(
                    f'Decks with this random seed have already been generatied. Please choose a different seed not in this list {used_seeds}.'
                    )
            else:
                self.seed = seed
        else:
            if len(used_seeds) == 0:
                self.seed = 0
            else:
                self.seed = max(used_seeds) + 1

        unshuffled_deck = np.array([0]*26 + [1]*26, dtype = np.int8) 
        np.random.seed(self.seed)
        self.decks = np.tile(unshuffled_deck, (num_decks, 1))
        np.array([np.random.shuffle(row) for row in self.decks])


    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.decks})"
    
    @get_size
    @write_timer
    def save_decks(self):
        np.save(f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy', self.decks) 
        #maybe save as a compressed file???