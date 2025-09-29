import numpy as np
import os
from typing import Callable
from datetime import datetime as dt
import pandas as pd

def gen_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This decorator is used to time deck generation.
        It takes the time and stores it in a csv "Deck_Stats" along with the deck type, number of decks, and radom seed.
        '''
        #print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        run_time = dt.now()- t0
        #print(f'Ran for {run_time} sec(s)')

        self = args[0]
        seed = self.seed
        num_decks = self.num_decks
        class_name = self.__class__.__name__

        # If Deck_Stats doesn't exist, create it
        if not os.path.exists('src/Deck_Stats.csv'):
            Deck_Stats = pd.DataFrame(columns=['deck_type',
                                               'num_decks', 
                                               'random_seed', 
                                               'gen_time', 
                                               'file_size', 
                                               'write_time', 
                                               'read_time'])
        else:
            Deck_Stats = pd.read_csv('src/Deck_Stats.csv')

        #Add a new row to the file with the runtime just found
        new_row = pd.DataFrame([{'deck_type': class_name,
                                'num_decks': num_decks, 
                                'random_seed': seed, 
                                'gen_time': run_time, 
                                'file_size': None, 
                                'write_time': None, 
                                'read_time': None}])
        Deck_Stats = pd.concat([Deck_Stats, new_row], ignore_index = True)
        Deck_Stats.to_csv('src/Deck_Stats.csv', index = False)

        return results
    return _wrapper

def write_read_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This decorator is used to time how long it takes to read and write a file of decks.
        Used when .save_decks() is called.
        It adds read and write time information to the associated row in "Deck_Stats."
        '''
        #print(f'{fun.__name__} called')

        #Time writing the file
        t0 = dt.now()
        results = fun(*args, **kwargs)
        write_time = dt.now()- t0
        #print(f'Ran for {write_time} sec(s)')

        self = args[0]
        seed = self.seed
        num_decks = self.num_decks
        class_name = self.__class__.__name__

        #Find the associated deck and load it, recording load time
        if self.__class__.__name__ == 'DeckStackNpy':
            t0 = dt.now()
            np.load(f'Decks/DeckStack_{seed}_{num_decks}.npy')
            read_time = dt.now()- t0
        elif self.__class__.__name__ == 'DeckStackBin':
            t0 = dt.now()
            np.fromfile(f'Decks/DeckStack_{seed}_{num_decks}.bin', dtype=np.int8)
            read_time = dt.now()- t0
        #print(f'Ran for {read_time} sec(s)')

        #Add write and read time to Deck_Stats
        #A row with this random seed and deck type must already exist since an instance must be created to run .save_decks()
        Deck_Stats = pd.read_csv('src/Deck_Stats.csv')
        if seed in Deck_Stats['random_seed'].values: 
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == class_name), 'write_time'] = write_time
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == class_name), 'read_time'] = read_time
            Deck_Stats.to_csv('src/Deck_Stats.csv', index = False)
        else: # should never actually happen since we check the seed in the class definition
            raise ValueError(f'No deck with this random seed found.')

        return results
    return _wrapper

def get_size(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This decorator finds the file size for a particular deck after its saved,
        and stores that time in Deck_Stats.
        Used when .save_decks() is called.
        '''

        result = fun(*args, **kwargs)
        self = args[0]
        class_name = self.__class__.__name__
        seed = self.seed

        #Find file path dependent on file type.
        if class_name == 'DeckStackNpy':
            file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy'
        elif class_name == 'DeckStackBin':
            file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.bin'

        #Find file size
        if os.path.exists(file_path):
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024*1024)
            #print(f"Saved file: {file_path}")
            #print(f"File size: {file_size_bytes} bytes ({file_size_mb:.2f} KB)")
        else:
            raise FileNotFoundError(f"Warning: File {file_path} not found.")
        
        #Store file size in associated row of Deck_Stats
        Deck_Stats = pd.read_csv('src/Deck_Stats.csv')
        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == class_name), 'file_size'] = file_size_mb
            Deck_Stats.to_csv('src/Deck_Stats.csv', index = False)
        else:
            raise ValueError(f'No deck with this random seed found.')

        return result
    return _wrapper