from DeckGeneration import DeckStack

import numpy as np
import os

# used_seeds = [int(file.split('_')[1]) for file in os.listdir('Decks')]
# new_seed = max(used_seeds) + 1
# print(new_seed)

test = DeckStack(1000000)
test.save_decks()

# test = np.load('Decks\DeckStack_7_10.npy')
# print(test)