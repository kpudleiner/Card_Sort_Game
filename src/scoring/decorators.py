import numpy as np
import os
from typing import Callable
from datetime import datetime as dt
import pandas as pd

def score_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This decorator is used to time deck scoring.
        It takes the time and stores it in a csv "score_stats" along with the deck type.
        '''
        #print(f'{fun.__name__} called')

        t0 = dt.now()
        results = fun(*args, **kwargs)
        run_time = dt.now()- t0
        #print(f'Ran for {run_time} sec(s)')

        self = args[0]
        class_name = self.__class__.__name__

        # If Deck_Stats doesn't exist, create it
        if not os.path.exists('score_stats.csv'):
            score_stats = pd.DataFrame(columns=['score_type',
                                               'score_time'])
        else:
            score_stats = pd.read_csv('score_stats.csv')

        #Add a new row to the file with the runtime just found
        new_row = pd.DataFrame([{'score_type': class_name,
                                'score_time': run_time }])
        score_stats = pd.concat([score_stats, new_row], ignore_index = True)
        score_stats.to_csv('score_stats.csv', index = False)

        return results
    return _wrapper
