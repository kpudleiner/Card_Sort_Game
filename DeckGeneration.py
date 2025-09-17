import numpy as np
import random
import os
from typing import Callable
from datetime import datetime as dt
import time

#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

def timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This is the modified version of the function that gets returned.
        '''
        print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        print(f'Ran for {dt.now()-t0} sec(s)')

        return results
    return _wrapper

def size(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        self = args[0]
        file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy'
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            print(f"Saved file: {file_path}")
            print(f"File size: {size_bytes} bytes ({size_bytes / 1024:.2f} KB)")
        else:
            print(f"Warning: File {file_path} not found.")
        return result
    return _wrapper

#Method 1: soter integer 0s and 1s as numpy arrays
class DeckStack:
    """
    A class to represent multiple shuffled decks.
    Takes the number of decks and random seed as input.
    
    """
    @timer
    def __init__(self, num_decks: int, seed: int = None):

        #self.seed = seed
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
    
    #@size
    @timer
    def save_decks(self):
        np.save(f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy', self.decks) 
        #maybe save as a compressed file???