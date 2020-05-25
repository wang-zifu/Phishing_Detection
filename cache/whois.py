import whois

class Whois_(Cache):
    def __init__(self):
        Cache.__init__(self)
        
    def get_data_whois_API(self, domain):
        self.dictionary = {}
        self.row = []
        try: 
            time.sleep(0.5)
            print(domain, ' API CALL 1')
            domain_ = whois.whois(domain)
            return domain_
        except:
            try:
                time.sleep(0.5)
                print(domain, ' API CALL 2')
                domain_ = whois.whois(domain)
                return domain_
            except:
                print('Error Whois API')
                return None
        
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