
class Features:
    def __init__(self, data=None):
        self.data = data

class LayerOneExtraction(Features):
    def __init__(self, data):
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

    def numTokenWords(self) -> int:
        """ Number of'.' excluding default domain dot """
        count = 0
        for character in self.data:
            if character == '.':
                count += 1
        if count == 0:
            return count 
        return count - 1