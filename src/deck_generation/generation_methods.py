import numpy as np
import os
import random
from src.deck_generation.decorators import gen_timer, write_read_timer, get_size

class DeckStackNpy:
    """
    A class to represent multiple shuffled decks.
    Takes the number of decks and random seed as input.
    If no random seed is specified, then find the largest existing seed and add one.

    """

    #@gen_timer
    def __init__(self, num_decks: int, seed: int = None):

        DECK_HALF_SIZE = 26

        self.num_decks = num_decks

        #Search existing decks to find next seed
        used_seeds_scored = [int(file.split('_')[1]) for file in os.listdir('Decks/Scored')]
        used_seeds_unscored = [int(file.split('_')[1]) for file in os.listdir('Decks/Unscored')]
        used_seeds = used_seeds_scored + used_seeds_unscored
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

        unshuffled_deck = np.array([0]*DECK_HALF_SIZE + [1]*DECK_HALF_SIZE, dtype = np.int8) 
        np.random.seed(self.seed)
        self.decks = np.tile(unshuffled_deck, (num_decks, 1))
        np.array([np.random.shuffle(row) for row in self.decks])


    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.decks})"
    
    #@get_size
    #@write_read_timer
    def save_decks(self):
        np.save(f'Decks/Unscored/DeckStack_{self.seed}_{self.num_decks}.npy', self.decks) 
