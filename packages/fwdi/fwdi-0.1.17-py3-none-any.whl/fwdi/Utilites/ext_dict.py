import pandas as pd

class ExtDict():
    
    @staticmethod
    def merge(a1:dict, a2:dict)->dict:
        a3 = dict(a1.items() | a2.items())
        return a3
    
    @staticmethod
    def to_pandas(data:dict)->pd.DataFrame:
        df = pd.DataFrame([data])

        return df