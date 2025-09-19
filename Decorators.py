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
            Deck_Stats = pd.DataFrame(columns=['num_decks', 
                                               'random_seed', 
                                               'gen_time', 
                                               'file_size', 
                                               'write_time', 
                                               'read_time'])
        else:
            Deck_Stats = pd.read_csv('Deck_Stats.csv')

        if seed in Deck_Stats['random_seed'].values: #theoretically shouldn't happen
            raise ValueError(
                    f'Decks with this random seed have already been generatied. Please choose a different seed.'
                    )
        else:
            new_row = pd.DataFrame([{'num_decks': num_decks, 
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

        np.load(f'Decks/DeckStack_{seed}_{num_decks}.npy')

        t0 = dt.now()
        Deck_Stats = pd.read_csv('Deck_Stats.csv')
        read_time = dt.now()- t0
        print(f'Ran for {read_time} sec(s)')

        if seed in Deck_Stats['random_seed'].values: #theoretically must happen
            Deck_Stats.loc[Deck_Stats['random_seed'] == seed, 'write_time'] = write_time
            Deck_Stats.loc[Deck_Stats['random_seed'] == seed, 'read_time'] = read_time
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return results
    return _wrapper

def get_size(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        self = args[0]

        file_path = f'Decks/DeckStack_{self.seed}_{self.num_decks}.npy'
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
            Deck_Stats.loc[Deck_Stats['random_seed'] == seed, 'file_size'] = file_size_mb
            Deck_Stats.to_csv('Deck_Stats.csv', index = False)

        else:
            raise ValueError(f'No deck with this random seed found.')

        return result
    return _wrapper