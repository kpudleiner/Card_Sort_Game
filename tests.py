from DeckGeneration import DeckStack

import numpy as np
import os


test = DeckStack(10000)
test.save_decks()

# test = np.load('Decks\DeckStack_0_10000.npy')
# print(test)

#Method one:
#DeckStack(10000)
#Time:
#file size
