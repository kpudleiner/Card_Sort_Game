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
player_wins_method1 = db.run_query(sql)
player_wins_method1['Method'] = 1
print(player_wins_method1)

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

player_wins_method2 = db.run_query(sql)
player_wins_method2['Method'] = 2
print(player_wins_method2)

combined_wins = pd.concat([player_wins_method1, player_wins_method2], ignore_index=True)
combined_wins.to_csv('player_wins.csv')

#Stats recorded during scoring are stored in "score_time_stats"
score_stats = pd.read_csv('score_time_stats.csv')
print(score_stats.head())
print(len(score_stats))

score_stats['score_time'] = pd.to_timedelta(score_stats['score_time'])

#Calculate averages and standard deviations for each method
stat_avgs = score_stats.groupby(['score_type']).agg(['mean', 'std']).reset_index()
stat_avgs[('score_time', 'mean')] = stat_avgs[('score_time', 'mean')].dt.total_seconds().round(5)
stat_avgs[('score_time', 'std')] = stat_avgs[('score_time', 'std')].dt.total_seconds().round(5)

print(stat_avgs)

