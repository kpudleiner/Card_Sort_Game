from DeckGeneration import DeckStack_npy, DeckStack_bin
import numpy as np
import os
import pandas as pd
import random

#Create 10 sets of 10,000 decks (each type)
#All run time and size information being saved to "Deck_Stats.csv"
for i in range(100):
    decks_npy = DeckStack_npy(10000)
    decks_npy.save_decks()
    decks_bin = DeckStack_bin(10000)
    decks_bin.save_decks()





# data = np.fromfile("Decks/DeckStack_9_10000.bin", dtype=np.int8)
# print(data)
# print(len(data))

Deck_Stats = pd.read_csv('Deck_Stats.csv')
print(Deck_Stats.head())
print(len(Deck_Stats))

#Method one:
#DeckStack(10000)
#Time:
#file size
