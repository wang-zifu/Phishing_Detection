from external.whois import WhoisCollection

class Features:
    def __init__(self, data=None):
        """ A features parent class. 
        Args:
            data (string): the observations.
        """
        self.data = data

class LayerOneExtraction(Features):
    def __init__(self, data):
        """ Initialise a detection 
        Args:
            Features.data (string): Inherit the observations
        """
        Features.__init__(self, data)

    def domain_length(self) -> int:
        """ Length of data """
        return len(self.data)
    
    def percentage_numeric(self) -> float:
        """ Percentage of Numerical Characters """
        count = 0
        for character in self.data:
            if character.isnumeric():
                count += 1 
        return round(float(count) / len(self.data), 2)
    
    def top_level_domain_length(self) -> int:
        """ Length of top-level domain """
        length = len(self.data.split('.')[-1])
        return length

    def second_level_domain_length(self) -> int:
        """ Length of second-level domain """
        length = len(self.data.split('.')[::1][0])
        return length

    def num_dots(self) -> int:
        """ Number of '.' excluding default domain dot """
        count = 0
        for character in self.data:
            if character == '.':
                count += 1
        if count == 0:
            return count 
        return count - 1

class LayerTwoExtraction(Features):
    def __init__(self, data, domain):
        Features.__init__(self, data)
        self.domain = domain

    def time_to_live(self):
        return self.data['TTL']

    def length_response(self):
        return self.data['length_response']

    def time_interval(self):
        pass

    def count_of_requests(self):
        pass

    def count_of_responses(self):
        pass

    def registrar_name(self):
        pass

    def creation_date(self):
        """ Requires Fix """ 
        whois = WhoisCollection()
        creation_date, registrar_name = whois.get_domain_data(self.domain)
        if creation_date == None:
            return 0
        return creation_date
