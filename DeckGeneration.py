
#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

import numpy as np
import random

#Method 1: soter integer 0s and 1s as numpy arrays

class DeckStack:
    #_global_seed = 0
    def __init__(self, num_decks, seed = None):

        self.seed = seed
        self.num_decks = num_decks

        unshuffled_deck = np.array([0]*26 + [1]*26)
        np.random.seed(self.seed)
        self.decks = np.tile(unshuffled_deck, (num_decks, 1))
        np.array([np.random.shuffle(row) for row in self.decks])

    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.decks})"
    
    def save_decks(self):
        np.save(f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy', self.decks)
    

