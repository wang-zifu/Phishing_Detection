import pandas as pd

class Data:
    def __init__(self, data):
        self._data = data
     
    def get_dataframe(self, **kwargs):
        rows = []
        _dictionary = {}
        for key, value in kwargs.items():
            _dictionary.update({key : value})
        rows.append(_dictionary)
        return pd.DataFrame(rows)
