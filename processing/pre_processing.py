from processing.features import LayerOneExtraction
from processing.data import Data

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

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

        self.observations_dataframe = self.get_dataframe(
            domain_length=domain_length,
            percentage_numeric=percentage_numeric,
            top_level_domain_length=top_level_domain_length,
            second_level_domain_length=second_level_domain_length,
            num_dots=num_dots
            )
        return self.observations_dataframe
    
    @staticmethod
    def data_split(dataset_train_columns, dataset_labels):
        X_train, X_test, Y_train, Y_test = train_test_split(
            dataset_train_columns, dataset_labels, test_size=0.05, shuffle=True)
        return X_train, X_test, Y_train, Y_test