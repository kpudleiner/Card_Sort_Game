# Overview
This repository contains the code to simulate the The Humble-Nishiyama Randomness Game. It simulates every possible combination of choices, simulates games, and finds the experimental probability that a player wins with the given choices.

---
## Quick-Start Guide

This project utilizes UV for version control. If you are unfamiliar with UV, please see [their doccumentation](https://docs.astral.sh/uv/guides/install-python/) for more information on its implementation. Once you have downloaded the repository, simply run `uv sync` to set up all necessary packages.

Over 5 million decks have already been scored. In order to create and score more decks, run `main.py` and it will prompt you through this process. 

If you wish to completely recreate the results, delete all decks in `Decks/Scored` as well as `src/scoring/player_wins.csv` and recreate all decks.
