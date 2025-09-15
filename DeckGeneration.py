
#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

import numpy as np
import random
import os

#Method 1: soter integer 0s and 1s as numpy arrays

class DeckStack:
    """
    A class to represent multiple shuffled decks.
    Takes the number of decks and random seed as input.
    
    """
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
            self.seed = max(used_seeds) + 1

        unshuffled_deck = np.array([0]*26 + [1]*26)
        np.random.seed(self.seed)
        self.decks = np.tile(unshuffled_deck, (num_decks, 1))
        np.array([np.random.shuffle(row) for row in self.decks])

    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.decks})"
    
    def save_decks(self):
        np.save(f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy', self.decks)
    

