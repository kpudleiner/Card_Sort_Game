from Generation_Methods import DeckStack_npy, DeckStack_bin
import numpy as np
import os
import pandas as pd
import random
import datetime as dt

#Run to Delete all decks and stats
#Uncomment if you want to run tests from begining

# folder_path = 'Decks'
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     os.remove(file_path)
# os.remove('Deck_Stats.csv')

#Create 20 sets of 10,000 decks (each type)
#All run time and size information being saved to "Deck_Stats.csv"

# for i in range(200):
#     decks_npy = DeckStack_npy(10000)
#     decks_npy.save_decks()
#     decks_bin = DeckStack_bin(10000)
#     decks_bin.save_decks()

Deck_Stats = pd.read_csv('Deck_Stats.csv')
print(Deck_Stats.head())
print(len(Deck_Stats))

Deck_Stats['gen_time'] = pd.to_timedelta(Deck_Stats['gen_time'])
Deck_Stats['write_time'] = pd.to_timedelta(Deck_Stats['write_time'])
Deck_Stats['read_time'] = pd.to_timedelta(Deck_Stats['read_time'])

Stat_Avgs = Deck_Stats.groupby(['deck_type', 'num_decks']).agg(['mean', 'std']).reset_index()

Stat_Avgs[('gen_time', 'mean')] = Stat_Avgs[('gen_time', 'mean')].dt.total_seconds().round(5)
Stat_Avgs[('write_time', 'mean')] = Stat_Avgs[('write_time', 'mean')].dt.total_seconds().round(5)
Stat_Avgs[('read_time', 'mean')] = Stat_Avgs[('read_time', 'mean')].dt.total_seconds().round(5)
Stat_Avgs[('file_size', 'mean')] = Stat_Avgs[('file_size', 'mean')].round(5)

Stat_Avgs[('gen_time', 'std')] = Stat_Avgs[('gen_time', 'std')].dt.total_seconds().round(5)
Stat_Avgs[('write_time', 'std')] = Stat_Avgs[('write_time', 'std')].dt.total_seconds().round(5)
Stat_Avgs[('read_time', 'std')] = Stat_Avgs[('read_time', 'std')].dt.total_seconds().round(5)
Stat_Avgs[('file_size', 'std')] = Stat_Avgs[('file_size', 'std')].round(5)

Stat_Avgs = Stat_Avgs.drop('random_seed', axis=1)

print(Stat_Avgs)

