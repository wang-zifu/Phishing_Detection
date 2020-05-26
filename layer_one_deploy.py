from detection.machine_learning import Model
from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
import pandas as pd
import logging

def layer_one_deploy():

    # Load a trained machine learning model 
    model = Model(layer=1, model_name='./detection/models/layer_one_model')
    if not model.read_model():
        logging.warning('Training a model')
        model.train_controller()
    
    # Initialise SEND 
    pipeline = DataPipe()
    pipeline.set_producer()
    
    # Initialise Consumer
    consumer = pipeline.get_consumer('test', 'test')
    for data in consumer:
        data = data.value.decode()
        # Level One Feature Extraction
        pre_processing = PreProcessing(data)
        processed_data = pre_processing.extraction()
        if not isinstance(processed_data, pd.DataFrame):
            logging.warning("Error Processing Observations.")
             
        processed_data_ = model.scale(processed_data)

        # Layer One Predictions
        prediction, probabilities = model.prediction(processed_data_)
        print(data, prediction, probabilities)

        pipeline.producer_send('test_y', {'prediction': str(prediction),
                                        'proabilities_benign': str(probabilities[0][0]),
                                        'probabilities_malicious': str(probabilities[0][1]),
                                        'domain': data})