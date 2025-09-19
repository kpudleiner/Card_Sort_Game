import numpy as np
import os
from typing import Callable
from datetime import datetime as dt
import pandas as pd

def gen_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This is the modified version of the function that gets returned.
        '''
        print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        run_time = dt.now()- t0
        print(f'Ran for {run_time} sec(s)')

        self = args[0]
        seed = self.seed
        num_decks = self.num_decks

        if not os.path.exists('Deck_Stats.csv'):
            Deck_Stats = pd.DataFrame(columns=['deck_type',
                                               'num_decks', 
                                               'random_seed', 
                                               'gen_time', 
                                               'file_size', 
                                               'write_time', 
                                               'read_time'])
        else:
            Deck_Stats = pd.read_csv('Deck_Stats.csv')

        new_row = pd.DataFrame([{'deck_type': self.__class__.__name__,
                                'num_decks': num_decks, 
                                'random_seed': seed, 
                                'gen_time': run_time.total_seconds(), 
                                'file_size': None, 
                                'write_time': None, 
                                'read_time': None}])
        Deck_Stats = pd.concat([Deck_Stats, new_row], ignore_index = True)
        Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        return results
    return _wrapper

def write_read_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This is the modified version of the function that gets returned.
        '''
        print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        write_time = dt.now()- t0
        print(f'Ran for {write_time} sec(s)')

        self = args[0]
        seed = self.seed
        num_decks = self.num_decks

        if self.__class__.__name__ == 'DeckStack_npy':
            t0 = dt.now()
            np.load(f'Decks/DeckStack_{seed}_{num_decks}.npy')
            read_time = dt.now()- t0
        elif self.__class__.__name__ == 'DeckStack_bin':
            t0 = dt.now()
            np.fromfile(f'Decks/DeckStack_{seed}_{num_decks}.bin', dtype=np.int8)
            read_time = dt.now()- t0

        print(f'Ran for {read_time} sec(s)')

        Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == self.__class__.__name__), 'write_time'] = write_time
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == self.__class__.__name__), 'read_time'] = read_time
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return results
    return _wrapper

def get_size(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        self = args[0]

        if self.__class__.__name__ == 'DeckStack_npy':
            file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy'
        elif self.__class__.__name__ == 'DeckStack_bin':
            file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.bin'
        if os.path.exists(file_path):
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024*1024)
            print(f"Saved file: {file_path}")
            print(f"File size: {file_size_bytes} bytes ({file_size_mb:.2f} KB)")
        else:
            print(f"Warning: File {file_path} not found.")

        self = args[0]
        seed = self.seed
        Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[(Deck_Stats['random_seed'] == seed) & (Deck_Stats['deck_type'] == self.__class__.__name__), 'file_size'] = file_size_mb
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return result
    return _wrapper