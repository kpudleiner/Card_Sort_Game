# Data Generation: Kailyn Pudleiner and Will Stanziano. 

For our project, we explored two different ways to generate and store a deck of cards. In both, we generated arrays of ones and zeros using an integer data type, but the means by which we do this and the storage methods differ.

## Methods

Method 1: Generates 2,000,000 "decks" of 52 cards by generating a two dimensional numpy array of randomly shuffled collection of 26 0's and 26 1's. Those are then saved into numpy array files (.npy) of 10,000 decks each.

Method 2: Generates 2,000,000 "decks" of 52 cards by using a for loop to generate a binary array of randomly shuffled collection of 26 0's and 26 1's. The collection of these are then saved into binary (.bin) files of 10,000 decks each.


## Results

For each method, we created 200 sets of 10,000 decks, leading to 2,000,000 decks. Using decorators, we recorded deck generation time, file size, read time, and write time. These values were stored in "Deck_Stats.csv" and the average were calculated. 

|Method        |Generation Time (s) |File Size (mb) |Write Time (s)    |Read Time (s)      |
|--------------|--------------------|---------------|------------------|-------------------|
|Method 1: NPY |0.01748 +- 0.00588  |0.49603 +- 0.0 |0.03114 +- 0.01711|0.11450 +- 0.04380 |
|Method 2: BIN |0.09503 +- 0.01027  |0.49591 +- 0.0 |0.01023 +- 0.01364|0.04184 +- 0.01340 |

At first glance, you may notice that method two wins in three out of the four categories. It has a much smaller read and write time, as well as a slightly smaller file size. However, it's generation time is much greater that of method one. This is likely due to the for loops present in method two that are noticeably absent form method one. When we add together the generation, read, and write times, method one and method two have extremely comparable times of 0.16312 and 0.1471 seconds respectively. The total time and storage difference is somewhat negligible between the two methods.

Some may argue that the extra time making the .bin file is unimportant since that will only be done once when the decks are created. However, there are a couple other problems with this method that may occur when scoring comes into play. Method two stores all the decks in a one-dimensional fashion instead of a two-dimensional one. This means we will have to continuously select the first 52 integers in order to score, instead of simply selecting the first array. It's also notable that numpy arrays have a myriad of functions that can assist in searching and scoring, which will likely be advantageous. Hence, despite the slightly smaller size and slightly faster read and write times of method 2, we believe method one will be more fortuitus in the long run.

