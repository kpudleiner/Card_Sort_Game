print('hello')
from src.Generation_Methods import DeckStack
# print('hello')
# test = DeckStack(3, 0)
# print(test.decks)

decks_npy = DeckStack(10000)
decks_npy.save_decks()
