from scoring_methods import ScoringDeck, ScoringDeckPd, score_all_unscored_decks, score_file
from deck_scoring_db_create import reset_db
from base_db import BaseDB
import numpy as np
import pandas as pd
import os
import shutil

# Method 1: 
reset_db()
score_all_unscored_decks('ScoringDeck')

db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite')

sql = """
SELECT * FROM deck_scores
"""
print(db.run_query(sql))

sql = """
SELECT * FROM player_wins
"""
print(db.run_query(sql))

#Move scored decks back to unscored folder
unscored_folder = "../../Decks/Unscored"
scored_folder = "../../Decks/Scored"
for file_name in os.listdir(scored_folder):
    file_path = os.path.join(scored_folder, file_name)

    destination_path = os.path.join(unscored_folder, file_name)
    shutil.move(file_path, destination_path)

# Method 2: 
reset_db()
score_all_unscored_decks('ScoringDeckPd')

db_path = 'deck_scoring.sqlite'
db = BaseDB(path='deck_scoring.sqlite')

sql = """
SELECT * FROM deck_scores
"""
print(db.run_query(sql))

sql = """
SELECT * FROM player_wins_view
"""
print(db.run_query(sql))


#Stats recorded during scoring are stored in "Deck_Stats"
score_stats = pd.read_csv('score_stats.csv')
print(score_stats.head())
print(len(score_stats))

score_stats['score_time'] = pd.to_timedelta(score_stats['score_time'])

#Calculate averages and standard deviations for each method
stat_avgs = score_stats.groupby(['score_type']).agg(['mean', 'std']).reset_index()

stat_avgs[('score_time', 'mean')] = stat_avgs[('score_time', 'mean')].dt.total_seconds().round(5)

stat_avgs[('score_time', 'std')] = stat_avgs[('score_time', 'std')].dt.total_seconds().round(5)


print(stat_avgs)

