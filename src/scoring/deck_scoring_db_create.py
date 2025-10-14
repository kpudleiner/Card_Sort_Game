from src.scoring.base_db import BaseDB
import numpy as np
import pandas as pd

def reset_db():
    """
    This function can be used to create or replace the database tables that contain deck scores.
    It will delete the 'deck_scores' and 'player_wins' table if they exist and create them again.
    It also creates the 'player_wins_view' that is used for the second scoring method.
    """

    db_path = 'src/scoring/deck_scoring.sqlite'
    db = BaseDB(path=db_path, create = True)

    sql = """
    DROP TABLE IF EXISTS deck_scores;
    """
    db.run_action(sql, commit=True)

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
    CREATE VIEW IF NOT EXISTS player_wins_view AS
    SELECT p1
        , p2
        , SUM(CASE WHEN p1_tricks > p2_tricks THEN 1 ELSE 0 END) AS p1_wins_tricks
        , SUM(CASE WHEN p2_tricks > p1_tricks THEN 1 ELSE 0 END) AS p2_wins_tricks
        , SUM(CASE WHEN p1_cards > p2_cards THEN 1 ELSE 0 END) AS p1_wins_cards
        , SUM(CASE WHEN p2_cards > p1_cards THEN 1 ELSE 0 END) AS p2_wins_cards
        , SUM(CASE WHEN p1_tricks = p2_tricks THEN 1 ELSE 0 END) AS draws_tricks
        , SUM(CASE WHEN p1_cards = p2_cards THEN 1 ELSE 0 END) AS draws_cards
    FROM deck_scores
    GROUP BY p1, p2
    ;
    """
    db.run_action(sql, commit=True)


    sql = """
    DROP TABLE IF EXISTS player_wins;
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
                sql = f"""
                INSERT INTO player_wins (
                    p1, p2, p1_wins_tricks, p2_wins_tricks, p1_wins_cards, p2_wins_cards, draws_tricks, draws_cards
                ) VALUES (
                    '{pattern}', '{pattern_2}', {0}, {0}, {0}, {0}, {0}, {0}
                );
                """
                db.run_action(sql, commit=True)

    return

#reset_db
