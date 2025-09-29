import os
import sqlite3
import numpy as np
import pandas as pd
sqlite3.register_adapter(np.int64, lambda x: int(x))
sqlite3.register_adapter(np.int32, lambda x: int(x))

class BaseDB:

    __slots__ = (
        '_connected',
        '_path',
        '_existed'
        )

    # Either 'dataframe' or 'list'
    RESULTS_TYPE = 'dataframe'
    
    def __init__(self, 
                 path: str,
                 create: bool = False
                ):
        
        self._connected = False
        self._path = os.path.normpath(path)
        self._check_exists(create)
        return
    
    def _connect(self, foreign_keys: bool = True) -> None:
        if not self._connected:
            self._conn = sqlite3.connect(self._path)
            self._curs = self._conn.cursor()
            if foreign_keys:
                self._curs.execute("PRAGMA foreign_keys=ON;")
            self._connected = True
        return
    
    def _close(self) -> None:
        self._conn.close()
        self._connected = False
        return
    
    def _rollback_and_close(self) -> None:
        self._conn.rollback()
        self._close()
        return
    
    def commit_and_close(self) -> None:
        self._conn.commit()
        self._close()
        return
    
    def _check_exists(self, create: bool) -> bool:
        self._existed = True
        path_parts = self._path.split(os.sep)
        
        n = len(path_parts)
        for i in range(n):
            part = os.sep.join(path_parts[:i+1])
            if not os.path.exists(part):
                self._existed = False
                if not create:
                    raise FileNotFoundError(f'{part} does not exist')
                if i == n-1:
                    print('Creating db')
                    self._connect()
                    self._close()
                else:
                    os.mkdir(part)
        return
    
    def _drop_views(self) -> None:
        views = self.run_query("SELECT name FROM sqlite_master WHERE type = 'view';")
        print(f'Dropping: {views}')
        for view in views.values:
            self.run_action(f"DROP VIEW {view[0]};")
        return

    def run_query(self, 
                  sql: str, 
                  params:tuple|dict = None,
                  keep_open: bool = False
                 ) -> list[tuple]:
        self._connect()
        try:
            if self.RESULTS_TYPE == 'dataframe':
                results = pd.read_sql(sql, self._conn, params=params)
            elif self.RESULTS_TYPE == 'list':
                if params is not None:
                    results = self._curs.execute(sql, params).fetchall()
                else:
                    results = self._curs.execute(sql).fetchall()
            else:
                raise ValueError(f'{self.RESULTS_TYPE} is not valid for RESULTS_TYPE')
        except Exception as e:
            raise type(e)(f'sql: {sql}\nparams: {params}') from e
        finally:
            if not keep_open:
                self._close()
        return results

    def run_action(self,
                   sql: str,
                   params: tuple|dict = None,
                   commit: bool = False,
                   keep_open: bool = False
                  ) -> int:
        self._connect()    
        try:
            if params is None:
                self._curs.execute(sql)
            else:
                self._curs.execute(sql, params)

            if commit:
                self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            self._close()
            raise type(e)(f'sql: {sql}\nparams: {params}') from e

        if not keep_open:
            self._close()
        return self._curs.lastrowid
    
    @staticmethod
    def generate_insert_sql(table_name: str, 
                            df: pd.DataFrame) -> str:
        columns = list(df.columns)
        
        sql = (f"INSERT INTO {table_name} ({', '.join(columns)} )\n"
               f"VALUES (:{', :'.join(columns)});")
        
        return sql
    
    def _load_table_from_df(self, 
                            df_path: str, 
                            table_name: str,
                            dtype: dict = None,
                            rename_columns: dict = None
                           ) -> None:
        if dtype is None:
            dtype = {}
        if rename_columns is None:
            rename_columns = {}
        
        df = pd.read_csv(df_path, dtype=dtype)
        df.rename(columns=rename_columns, inplace=True)
        
        sql = self.generate_insert_sql(table_name, df)
        
        for row in df.to_dict(orient='records'):
            self.run_action(sql, row, keep_open=True)
        self.commit_and_close()
        return
    
        
    

    

    