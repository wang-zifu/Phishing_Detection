from processing.features import LayerOneExtraction
from processing.data import Data

from sklearn.preprocessing import StandardScaler

class PreProcessing(Data):
    def __init__(self, data):
        Data.__init__(self, data)

    def _check_observation(self):
        """ Check if data is None and is numeric"""
        if not self._data:
            self._data = None
        if self._data.isnumeric():
            self._data = None
        return self._data
    
    def scale_observations(self, observations_dataframe):
        scaler = StandardScaler()
        observations_dataframe_scaled = scaler.transform(observations_dataframe)
        return observations_dataframe_scaled

    def extraction(self):
        valid_data = self._check_observation()
        if not valid_data:
            return 0
        # Begin Extraction Process
        layer_one_process = LayerOneExtraction(valid_data)

        domain_length = layer_one_process.domain_length()
        percentage_numeric = layer_one_process.percentage_numeric()
        top_level_domain_length = layer_one_process.top_level_domain_length()
        second_level_domain_length = layer_one_process.second_level_domain_length()
        num_dots = layer_one_process.num_dots()
        top_level_domain = layer_one_process.top_level_domain()

        observations_dataframe = self.get_dataframe(
            domain_length=domain_length,
            percentage_numeric=percentage_numeric,
            top_level_domain_length=top_level_domain_length,
            second_level_domain_length=second_level_domain_length,
            num_dots=num_dots,
            top_level_domain=top_level_domain
        )
        return observations_dataframe

    