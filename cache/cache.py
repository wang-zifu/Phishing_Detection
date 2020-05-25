import pandas
import os 

class Cache:
    def __init__(self):
        self._cache_data = None
        
    def set_cache(self, filename):
        """ Set the cache file """
        self._cache_filename = filename
        if os.path.exists(self._cache_filename):
            self._cache_data = pd.read_csv(self._cache_filename)
        else:
            return 0
        
    def add_data_cache(self, data):
        if len(data) > 0:
            cache_update = pd.DataFrame(data)
            cache_update = cache_update.reset_index(drop=True)
            frames = [self._cache_data, cache_update]
            self._cache_data = pd.concat(frames)
            
    def update_cache_file(self):
        self._cache_data.to_csv(self._cache_filename, index=False)