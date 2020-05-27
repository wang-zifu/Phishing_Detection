from processing.features import LayerOneExtraction
from processing.features import LayerTwoExtraction

from processing.data import Data

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class PreProcessing(Data):
    def __init__(self, data):
        Data.__init__(self, data)

    def _check_observation(self):
        """ Check if data is None and is numeric"""
        if not self.domain:
            self.domain = None
        if self.domain.isnumeric():
            self.domain = None
        return self.domain

    def extraction(self, layer):
        self.domain = str(self._data['domain'])[:-1]
        self.layer_two_features_pre = self._data['data']
        
        valid_domain = self._check_observation()

        if not valid_domain:
            return 0
        # Begin Extraction Process
        if layer == 1:
            layer_one_process = LayerOneExtraction(valid_domain)

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
        elif layer == 2:
            layer_two_process = LayerTwoExtraction(self.layer_two_features_pre, self.domain)
            
            time_to_live = layer_two_process.time_to_live()
            length_response = layer_two_process.length_response()
            creation_date = layer_two_process.creation_date()
            # registrar_name = layer_two_process.registrar_name()

            self.observations_dataframe = self.get_dataframe(
                time_to_live=time_to_live,
                length_response=length_response,
                creation_date=creation_date,
            )

        return self.observations_dataframe
    
    @staticmethod
    def data_split(dataset_train_columns, dataset_labels):
        X_train, X_test, Y_train, Y_test = train_test_split(
            dataset_train_columns, dataset_labels, test_size=0.05, shuffle=True)
        return X_train, X_test, Y_train, Y_test