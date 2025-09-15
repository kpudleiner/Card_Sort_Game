from DeckGeneration import DeckStack

import numpy as np
test = DeckStack(3, 0)
print(test.decks)
print(test.seed)
test.save_decks()