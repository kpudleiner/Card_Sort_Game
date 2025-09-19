from DeckGeneration import DeckStack_npy, DeckStack_bin
import numpy as np
import os
import pandas as pd
import random

#method1_generation_timer = []
test = DeckStack_bin(10000)
test.save_decks()
print(type(test))

# test2 = DeckStack_npy(10000)
# test2.save_decks()



# data = np.fromfile("Decks/DeckStack_9_10000.bin", dtype=np.int8)
# print(data)
# print(len(data))

print(pd.read_csv('Deck_Stats.csv'))

#Method one:
#DeckStack(10000)
#Time:
#file size
