# Data Generation: Kailyn Pudleiner and Will Stanziano. 

For our project, we explored two different ways to generate and store a deck of cards. In both, we generated arrays of ones and zeros, but the means by which we do this and the storage methods differ.

## Methods

Method 1: Generates 1,000,000 "decks" of 52 cards by generating a binary array of randomly shuffled collection of 26 0's and 26 1's, and saves these into 100 numpy array files of 10,000 decks each.

Method 2: Generates 1,000,000 "decks" of 52 cards by generating a binary array of randomly shuffled collection of 26 0's and 26 1's and saves these into 100 binary files of 10,000 decks each.


## Results

For each method, we created 100 sets of 10,000 decks, leading to 1,000,000 decks. Using decorators, we recorded deck generation time, file size, read time, and write time. These values were stored in "Deck_Stats.csv" and the average were calculated. 

|Method        |Generation Time (s) |File Size (mb) |Write Time (s)    |Read Time (s)      |
|--------------|--------------------|---------------|------------------|-------------------|
|Method 1: NPY |0.01748 +- 0.00588  |0.49603 +- 0.0 |0.03114 +- 0.01711|0.11450 +- 0.04380 |
|Method 2: BIN |0.09503 +- 0.01027  |0.49591 +- 0.0 |0.01023 +- 0.01364|0.04184 +- 0.01340 |

At first glance, you may notice that method two wins in three out of the four categories. It has a much smaller read and write time, as well as a slightly smaller file size. However, it's generation time is almost time times that of method one. This is likely due to the for loops present in method two that are noticably absent form method one. When we add together the generation, read, and write times, method one actually has a smaller total time of 0.098138 seconds versus 0.11842 seconds for method two. The differences now become more negligable between the two methods

Some may argue that the extra time making the .bin file is unimportant since that will only be done once when the decks are created. However, there are a couple other problems with this method that may come down the road with searching. Method two stores all the decks in a one-dimensional fashion instead of a two-dimensional one like method one. This means we will have to continuously select the first 52 integers in order to score, instead of simply selecting the first array. It's also notable that npy arrays have a miriad of functions that can assist in searching and scoring, as opposed to a simple array.

