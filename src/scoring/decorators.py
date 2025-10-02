import numpy as np
import os
from typing import Callable
from datetime import datetime as dt
import pandas as pd

def score_timer(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        '''
        This decorator is used to time deck scoring.
        It takes the time and stores it in a csv "Score_Stats" along with the deck type.
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
            Score_Stats = pd.DataFrame(columns=['score_type',
                                               'score_time', 
                                               'view_time'])
        else:
            Score_Stats = pd.read_csv('score_stats.csv')

        #Add a new row to the file with the runtime just found
        new_row = pd.DataFrame([{'deck_type': class_name,
                                'gen_time': run_time }])
        Score_Stats = pd.concat([Score_Stats, new_row], ignore_index = True)
        Score_Stats.to_csv('score_stats.csv', index = False)

        return results
    return _wrapper
