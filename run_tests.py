from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods import score_all_unscored_decks, save_player_scores
from src.scoring.base_db import BaseDB

# for i in range(10):
#     print(i)
#     decks_npy = DeckStackNpy(10000)
#     decks_npy.save_decks()

db = BaseDB(path='src/scoring/deck_scoring.sqlite')
sql = """
    SELECT COUNT(*) from deck_scores;
    """
print(db.run_query(sql))

score_all_unscored_decks()

print(db.run_query(sql))