
#Testing two methods of creating randomly shuffled deck stacks.
# - Method 1: store integers 0s and 1s as numpy arrays
# - Method 2: store as .bin

import numpy as np
import random

#Method 1: soter integer 0s and 1s as numpy arrays

#General Creation Method
# np.random.seed(1)
# num_decks = 3
# all_decks = np.empty((num_decks, 52))
# for i in range(num_decks):
#     new_deck = np.array([0] * 26 + [1] * 26)

#     np.random.shuffle(new_deck)
#     #print(new_deck)

#     all_decks[i] = new_deck

#     #all_decks = np.append(all_decks, new_deck, axis = 0)

#     print(all_decks)
#     np.save('test.npy', all_decks)
#     loaded = np.load('test.npy')
#     print(loaded)
#.bin  vs .npy


class DeckStack:
    #_global_seed = 0
    def __init__(self, num_decks, seed = None):

        self.seed = seed
        np.random.seed(self.seed)

        self.num_decks = num_decks

        unshuffled_deck = np.array([0]*26 + [1]*26)

        self.decks = np.tile(unshuffled_deck, (num_decks, 1))

        np.array([np.random.shuffle(row) for row in self.decks])

    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.decks})"
    

print('hello')

test = DeckStack_2(3, 0)
#print(test)
print(test.decks)
print(test.seed)