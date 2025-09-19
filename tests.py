from DeckGeneration import DeckStack_npy, DeckStack_bin
import numpy as np
import os
import pandas as pd
import random

#Run to Delete all decks and stats
#Uncomment if you want to run tests from begining

# folder_path = 'Decks'
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     os.remove(file_path)
# os.remove('Deck_Stats.csv')

#Create 10 sets of 10,000 decks (each type)
#All run time and size information being saved to "Deck_Stats.csv"

# for i in range(100):
#     decks_npy = DeckStack_npy(10000)
#     decks_npy.save_decks()
#     decks_bin = DeckStack_bin(10000)
#     decks_bin.save_decks()

data = np.fromfile("Decks/DeckStack_9_10000.bin", dtype=np.int8)
print(data)
print(len(data))

Deck_Stats = pd.read_csv('Deck_Stats.csv')
print(Deck_Stats.head())
print(len(Deck_Stats))

Deck_Stats['gen_time'] = pd.to_timedelta(Deck_Stats['gen_time'])
Deck_Stats['write_time'] = pd.to_timedelta(Deck_Stats['write_time'])
Deck_Stats['read_time'] = pd.to_timedelta(Deck_Stats['read_time'])

#Calculate the averages for each type of deck
Decks_npy = Deck_Stats[Deck_Stats['deck_type'] == 'DeckStack_npy']
Decks_bin = Deck_Stats[Deck_Stats['deck_type'] == 'DeckStack_bin']

print(Decks_npy.head())
print(Decks_bin.head())

print(f'NPY Decks \n Generation Time: {Decks_npy['gen_time'].mean()} \n File Size: {Decks_npy['file_size'].mean()} \n Write Time: {Decks_npy['write_time'].mean()} \n Read Time: {Decks_npy['read_time'].mean()}')

print(f'Bin Decks \n Generation Time: {Decks_bin['gen_time'].mean()} \n File Size: {Decks_bin['file_size'].mean()} \n Write Time: {Decks_bin['write_time'].mean()} \n Read Time: {Decks_bin['read_time'].mean()}')

#Method one:
#DeckStack(10000)
#Time:
#file size
