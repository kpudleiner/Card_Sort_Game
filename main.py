print('hello')
from src.generation_methods import DeckStackBin, DeckStackNpy
# print('hello')
# test = DeckStack(3, 0)
# print(test.decks)

decks_npy = DeckStackBin(10000)
decks_npy = DeckStackNpy(10000)
decks_npy.save_decks()
