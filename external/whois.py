import whois
import pandas as pd
import os 

"""
NEEDS RE-WRITING AS A CACHING TECHNOLOGY 
"""
class Cache:
    def __init__(self):
        self.set_cache_file()
        
    def set_cache_file(self):
        self._cache = pd.read_csv('./external/whoisCache.csv')

    def update_obj_cache(self):
        if len(self.row) > 0:
            cache_update = pd.DataFrame(self.row)
            cache_update = cache_update.reset_index(drop=True)
            frames = [self._cache, cache_update]
            self._cache = pd.concat(frames)
            
    def update_cache_csv(self):
        self._cache.to_csv(self.cache_name, index=False)


class WhoisCollection(Cache):
    def __init__(self):
        Cache.__init__(self)

    def get_data_whois_API(self, domain):
        self.dictionary = {}
        self.row = []
        try: 
            time.sleep(0.5)
            whois_data = whois.whois(domain)
            return whois_data
        except:
            return
        
    def get_data_cache(self, domain):
        for index_j, row_j in self._cache.iterrows():
            if domain == row_j['IP']:
                data = self._cache[self._cache['IP'] == domain]
                creation_date = data['creation_date']
                registrar_name = data['registrar_name']
                return str(creation_date).split()[1], str(registrar_name).split()[1]
        return None, None
    
    def get_domain_data(self, domain):
        # Check Cache for data
        domain_info, registrar_name = self.get_data_cache(domain)
        if domain_info == None:
            # Get data from API
            print('API Call: ', domain)
            domain_API = self.get_data_whois_API(domain)
            if domain_API != None:
                if isinstance(domain_API.creation_date, (list)):
                    creation_date = str(domain_API.creation_date[0])[:4]
                else:
                    creation_date = str(domain_API.creation_date)[:4]
                registrar_name = str(domain_API.registrar)
                self.dictionary.update({
                    'IP': domain,
                    'creation_date': creation_date,
                    'registrar_name': registrar_name
                })
                self.row.append(self.dictionary)
                self.update_obj_cache()
                return creation_date, registrar_name
            else:
                return None, None
        else:
            print('Cache: ', domain)
            return domain_info,registrar_name

def fix_cache():
    import numpy as np
    dataframe = pd.DataFrame()
    dataset = pd.read_csv('./detection/google.csv')
    cache = pd.read_csv('./external/whoisCache.csv')
    
    for index in dataset['domain']:
        
        dataset_ = cache.loc[cache['IP'] == index]
        dataset_ = dataset_['creation_date'].values[0]

        dataset.loc[dataset['domain'] == index, 'creation_date'] = dataset_
        
    dataset.to_csv('./google_updated.csv')

