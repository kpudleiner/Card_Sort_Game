### Overview
This repository contains the code to simulate the The Humble-Nishiyama Randomness Game. It simulates every possible combination of choices, simulates games, and finds the experimental probability that each player wins with the given choices.

### Files
- **Generation_Methods.py**: Contains methods for generating playing card decks, which are represented by arrays of zeros and ones.
- **Decorators.py**: Decorators used in **Generation_Methods.py** in order to time methods and find the size of decks.
- **run_tests.py** Code to generate 2,000,000 decks for each type of deck, store run times, and calculate averages.