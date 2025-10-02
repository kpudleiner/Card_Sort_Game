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