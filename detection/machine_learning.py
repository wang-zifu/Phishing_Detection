import pickle 
import logging

class Model:
    def __init__(self, threshold=None, model_name=None):
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

    def read_model(self):
        """ Read model from disk and store in memory """
        self.trained_model = pickle.load(open(self.trained_model_name, 'rb'))
        logging.warning('Model loaded')

    def train(self):
        """ Train a model if an existing one does not exist """
        pass
    
    def prediction(self, data):
        """ Use trained model to get probability scores and prediction binary """
        probabilities = self.trained_model.predict_proba(data)
        predictions = self.trained_model.predict(data)
        return predictions, probabilities
        