from DeckGeneration import DeckStack_npy
import numpy as np
import os
import pandas as pd

#method1_generation_timer = []
test = DeckStack_npy(10000)
test.save_decks()

test2 = DeckStack_npy(10000)
test2.save_decks()

print(pd.read_csv('Deck_Stats.csv'))

#Method one:
#DeckStack(10000)
#Time:
#file size
