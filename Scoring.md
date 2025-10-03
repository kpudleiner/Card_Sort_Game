# Scoring: Kailyn Pudleiner and Will Stanziano. 

For the scoring section of the project, we explored a few different routes for the scoring algorithm, and focused most of our attention on cutting down the write time of the scoring information. For our final method, we ended up creating a class: ScoringDeckPd, a representation of a deck, that has methods to both sort and save the scoring information. The class stores to string representation of the deck, and performs the scoring method ._score_deck. This method takes the deck and player choices as input. It finds the first instance of each pattern, returns them, and locates pattern that occurs first (also taking into account if the pattern is not found). It then discards those cards and incriments the winning players count. It utilizes string methods such as .find to find the pattern and simple indexing to get rid of cards. An example of the logic can be found below.

P1 Choice: 111\
P2 Choice: 001\
Deck: 1101011110001011100110110010101000011001000100011000

### Round 0:
|P1 Tricks  |P2 Tricks  |P1 Cards  |P2 Cards  |
|-----------|-----------|----------|----------|
|0          |0          |0         |0         |

### Round 1: 
11010<u>111</u> **|** 10<u>001</u>011100110110010101000011001000100011000
|P1 Tricks  |P2 Tricks  |P1 Cards  |P2 Cards  |
|-----------|-----------|----------|----------|
|1          |0          |8         |0         |

### Round 2:

10<u>001</u> **|** 0<u>111</u>001101100101010000110010001000110001
|P1 Tricks  |P2 Tricks  |P1 Cards  |P2 Cards  |
|-----------|-----------|----------|----------|
|1          |1          |8         |5         |

This pattern would continue until there are not enough cards left, or neither pattern is found. The method then outputs a single dictionary with the deck, player 1s choice, player 2s choice, player 1's tricks, player 2's tricks, player 1's cards, and player 2's cards. A seperate method calls this scoring method while cycling through all 56 player choice combinations. These 56 results are put into a pandas dataframe, which is then added to the deck_score table of the deck_scoring.sqlite database. In order to summarize the wins and losses for each of the 56 player combinations, we created a view. The view tallies when player one has more tricks than player two, etc, and summarizes that information in a table.That table is then what was saved to the csv. There is then a function to be called on one of the .npy files containing thousands of decks, which goes through and applys this method to each deck. We decided to create an "Unscored" folder withing our "Decks
 folder. The method searches the Unscored forlder, scores a whole file, and then moves it to the "Scored" folder. We plan to alter our generation methods to automatically output the decks to the unscored foler. This will make it easy to add new decks without scoring everything again. Below are more details about how we came to this method.

## String versus Array

Based on part one of the project, we decided to generate the decks as numpy arrays of 0s and 1s, and store them as .npy files. This means we then read the decks back in as arrays of integers as we wrote them. However, after begining to score the decks in this manner, it quickly became evident that scoring them as strings would likely be easier. For example, to find the first iteration of a sequence of three digits, strings have a very convenient .find() method, instead of incrimenting through the whole deck manually. Additionally, strings serve as easy dictionary keys, which is something we had in our original code. Hence, for these reasons we decided to represent the deck as a single string of 1s and 0s instead of an array of integers. We plan to go back and edit our generation methods to make it more compatable with out search method.

## Storage Method

Based on the fact that we would need to store over 100 million rows of scoring information, we decided that it would be best to store these in a sqlite databsae. Hence, we utilized BaseDB from databases to create a database. However, the best way to go about adding scores to the database proved difficult. Below are the two different methods we implimented.

**Method 1 (ScoringDeck)**: This method utilizes two database tables: 'deck_scores,' which stores each deck and player combination and its associated score and 'player_wins,' which keeps a running tally of all 56 player combinations and their wins and draws. Every time a deck is scored, the database is opened and the results are input into the 'deck_scores' table. Then, it is opened again to find the current values of 'player_wins.' These values are updated based on who had more tricks/cards, and the database is opened again to input the new values. This method worked, but was extremely slow, as to score one deck (with 56 combinations), the database was opened 168 times.

**Method 2 (ScoringDeckPd)**: This method looked to improve and simplify Method 1. It utilized the same scoring logic above, but instead of openeing the database for every player combination for every deck, it intermediately stores the scores in a pandas dataframe. For a single deck, a combination of player choices is scored, and then that information is added as a row to the dataframe. After all 56 combinations have been scored, each row is added to the 'deck_scores' table while keeping it open the whole time. This way, the database is opened once instead of 168 times per deck. To find the 'player_wins' statistics, we decided to create a view of 'deck_scores' instead of incrimenting it as we go and storing it as a seperate table. Hence, the view is selected once at the end, and takes a negligible amount of time to do this single operation.


## Results

To test these methods, we moved 5 files of 10,000 decks into the "Unscored" folder. For the sake of time, we only did the first 100 decks of each file as our first method takes quite some time. We created a decorator to time how long it takes to score one singe deck all 56 ways and store that information. The timing results can be seen below.

|Method        |Generation Time (s) | Database Size (KB)|
|--------------|--------------------|-------------------|
|Method 1 (ScoringDeck): |0.68061  +/-  0.12531 | 12,544 |
|Method 2 (ScoringDeckPd):  |0.03959 +/- 0.01076 | 12,544 |

As you can see, method two vastly improved the time it takes to score a deck. This isn't surprising since the opening and closing the database is expensive when it comes to time, and we decreased the times it was opening form 156 to one. The database sizes are the same, as the addition of one small table for method one doesn't have a substantial effect.

## Conclusion

Overall, exploring these multiple methods demonstrated how important it is to optimize the write time of your data. We were able to cut down time by an order of magnitude simply by altering how often the databse was open. Hence, we will move forward with method 2 and make the changes to our generation methods to make them mroe compatable. 
