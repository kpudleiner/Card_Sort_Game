from base_db import BaseDB
import numpy as np
import pandas as pd

db_path = 'deck_scoring.sqlite'
db = BaseDB(path=db_path)

sql = """
CREATE TABLE IF NOT EXISTS deck_scores (
    deck TEXT,
    p1 TEXT,
    p2 TEXT,
    p1_tricks INTEGER,
    p2_tricks INTEGER,
    p1_cards INTEGER,
    p2_cards INTEGER,
    PRIMARY KEY(deck, p1, p2)
);
"""
db.run_action(sql, commit=True)

sql = """
DROP TABLE player_wins;
"""

db.run_action(sql, commit=True)

sql = """
CREATE TABLE IF NOT EXISTS player_wins (
    p1 TEXT,
    p2 TEXT,
    p1_wins_tricks INTEGER,
    p2_wins_tricks INTEGER,
    p1_wins_cards INTEGER,
    p2_wins_cards INTEGER,
    draws_tricks INTEGER,
    draws_cards INTEGER,
    PRIMARY KEY(p1, p2)
);
"""

db.run_action(sql, commit=True)

patterns = ['000', '001', '010', '011', '100', '101', '110', '111']
for pattern in patterns:
    for pattern_2 in patterns:
        if pattern != pattern_2:
            print(pattern, pattern_2)
            sql = f"""
            INSERT INTO player_wins (
                p1, p2, p1_wins_tricks, p2_wins_tricks, p1_wins_cards, p2_wins_cards, draws_tricks, draws_cards
            ) VALUES (
                '{pattern}', '{pattern_2}', {0}, {0}, {0}, {0}, {0}, {0}
            );
            """
            db.run_action(sql, commit=True)

sql = """
SELECT * FROM player_wins
"""

print(db.run_query(sql))