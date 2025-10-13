from src.deck_generation.generation_methods import DeckStackNpy

for i in range(10):
    print(i)
    decks_npy = DeckStackNpy(10000)
    decks_npy.save_decks()