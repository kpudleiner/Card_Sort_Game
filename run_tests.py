from src.deck_generation.generation_methods import DeckStackNpy
from src.scoring.scoring_methods import score_all_unscored_decks, save_player_scores
from src.scoring.base_db import BaseDB
from src.scoring.deck_scoring_db_create import reset_db
import pandas as pd

for i in range(2):
    decks_npy = DeckStackNpy(10000)
    decks_npy.save_decks()

#reset_db()

db = BaseDB(path='src/scoring/deck_scoring.sqlite')
sql = """
    SELECT COUNT(*) from deck_scores;
    """
print(db.run_query(sql))

score_all_unscored_decks()

print(db.run_query(sql))


save_player_scores()

# print(pd.read_csv('src/scoring/player_wins.csv'))