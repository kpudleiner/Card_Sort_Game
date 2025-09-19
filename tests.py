from DeckGeneration import DeckStack_npy
import numpy as np
import os
import pandas as pd

# deck_stats = pd.DataFrame(columns = ['num_decks', 
#                              'random_seed', 
#                              'gen_time', 
#                              'file_size', 
#                              'save_time', 
#                              'load_time'])
# deck_stats.to_csv('Deck_Stats.csv')

#method1_generation_timer = []
test = DeckStack_npy(10000)
test.save_decks()

test = pd.read_csv('Deck_Stats.csv')
print(test)

#Method one:
#DeckStack(10000)
#Time:
#file size
