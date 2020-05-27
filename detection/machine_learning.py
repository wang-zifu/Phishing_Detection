import pickle 
import logging
from sklearn.preprocessing import StandardScaler
from processing.pre_processing import PreProcessing
from sklearn.neural_network import MLPClassifier
import pandas as pd 

layer_one_columns = ['dLength', 'domainNumChar', 'lengthTLD', 'lengthSLD', 'numTokenWord']
layer_two_columns = ['creation_date', 'ttl', 'length_response']
class Model:
    def __init__(self, layer, threshold=None, model_name=None):
        """ Initialise a detection 
        Args:
            threshold (float): The triage value to control observations through
                the layers of prediction.
            model (bytes): A filename to a trained model. 
            Default (None)
        """
        self.threshold = threshold
        self.trained_model_name = model_name
        self.trained_model = None
        self.layer = layer

    def read_model(self):
        """ Read model from disk and store in memory """
        if not self.trained_model:
            return 0
        self.trained_model = pickle.load(open(self.trained_model_name, 'rb'))
        logging.warning('Model loaded')

    def train_controller(self):
        """ Train a model if an existing one does not exist """
        self.dataset = pd.read_csv('./detection/google_updated.csv')
        self.dataset_labels = self.dataset[['label']]
        # Needs fix 
        self.dataset.loc[self.dataset['creation_date'] == 'None'] = 0
        self.dataset.loc[self.dataset['creation_date'] == 'befo'] = 0
        self.dataset.loc[self.dataset['creation_date'] == 'Befo'] = 0
        self.dataset.loc[self.dataset['creation_date'] == '0-UA'] = 0

        if self.layer == 1:
            self.dataset_train_columns = self.dataset[layer_one_columns]
            X_train, self.X_test, Y_train, self.Y_test = PreProcessing.data_split(self.dataset_train_columns, self.dataset_labels)
            self.trained_model = self.model_train(X_train, Y_train, 5)
        elif self.layer == 2:
            self.dataset_train_columns = self.dataset[layer_two_columns]
            X_train, X_test, Y_train, Y_test = PreProcessing.data_split(self.dataset_train_columns, self.dataset_labels)
            self.trained_model = self.model_train(X_train, Y_train, 3)
        logging.warning('Model training is complete.')

    def model_train(self, X_train, Y_train, size):
        self.scaler = StandardScaler()
        self.scaler.fit(X_train)
        self.X_train = self.scaler.transform(X_train)
        mlp = MLPClassifier(hidden_layer_sizes=(size,size,size),max_iter=500, activation='tanh')
        mlp.fit(self.X_train,Y_train)
        return mlp

    def scale(self, data):
        return self.scaler.transform(data)

    def prediction(self, data):
        """ Use trained model to get probability scores and prediction binary """
        probabilities = self.trained_model.predict_proba(data)
        predictions = self.trained_model.predict(data)
        return predictions, probabilities
        
