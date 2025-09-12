
#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

import numpy as np
import random

#Method 1: soter integer 0s and 1s as numpy arrays
np.random.seed(1)
num_decks = 3
all_decks = np.empty((num_decks, 52))
for i in range(num_decks):
    new_deck = np.array([0] * 26 + [1] * 26)

    np.random.shuffle(new_deck)
    #print(new_deck)

    all_decks[i] = new_deck

    #all_decks = np.append(all_decks, new_deck, axis = 0)

    print(all_decks)
    np.save('test.npy', all_decks)
    loaded = np.load('test.npy')
    print(loaded)

#.bin  vs .npy


class DeckStack:
    _global_seed = 0
    def __init__(self, num_decks, seed = 1):
        self.seed = DeckStack._global_seed
        DeckStack._global_seed += 1

        # Set the seed for reproducible shuffling
        random.seed(self.seed)

        self.num_decks = num_decks
        
        self.all_decks = np.empty((num_decks, 52))
        for i in range(num_decks):
            new_deck = np.array([0] * 26 + [1] * 26)
            np.random.shuffle(new_deck)
            #print(new_deck)

            self.all_decks[i] = new_deck
        random.shuffle(self.cards)

    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.cards})"

    def reset(self):
        """Reset the deck using the same seed as the original initialization."""
        random.seed(self.seed)
        self.cards = np.array([0] * 26 + [1] * 26)
        random.shuffle(self.cards)

    random_seed = 1
    cards = np.random.shuffle(np.array([0] * 26 + [1] * 26))
    def update_random_seed(self, random_seed):
        random_seed += 1

def create_decks(num_decks)
