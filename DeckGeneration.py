
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


#More robust class version
class DeckStack:
    #_global_seed = 0
    def __init__(self, num_decks, seed = None):

        if not seed:
            print('in loop')
            print(DeckStack._global_seed)
            self.seed = DeckStack._global_seed
            DeckStack._global_seed += 1
            print(DeckStack._global_seed)
            np.random.seed(self.seed)
        else:
            self.seed = seed

        self.num_decks = num_decks
        
        self.all_decks = np.empty((num_decks, 52))
        for i in range(num_decks):
            new_deck = np.array([0] * 26 + [1] * 26)
            np.random.shuffle(new_deck)

            self.all_decks[i] = new_deck

        # np.random.randint(0,2, size = (num_decks, 52))

    def __repr__(self):
        return f"DeckStack(seed={self.seed}, cards={self.all_decks})"

    def reset_random_seed(self, random_seed):
        DeckStack._global_seed = 0


print('hello')

test = DeckStack(1000)
#print(test)
print(test.all_decks[900])
print(test.seed)

