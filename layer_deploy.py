from detection.machine_learning import Model
from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
import pandas as pd
import logging



def layer_deploy(layer, consumer_t, producer_t):
    # Load a trained machine learning model 
    model = Model(layer, model_name='./detection/models/layer_one_model')
    if not model.read_model():
        logging.warning('Training a model')
        model.train_controller()
    
    # Initialise SEND 
    pipeline = DataPipe()
    pipeline.set_producer()
    
    # Initialise Consumer
    consumer = pipeline.get_consumer_json(consumer_t, 'test')
    for data in consumer:
        data = data.value

        # Level One Feature Extraction
        pre_processing = PreProcessing(data)

        processed_data = pre_processing.extraction(layer)

        if not isinstance(processed_data, pd.DataFrame):
            logging.warning("Error Processing Observations.")
        logging.warning("Processing Observations.")
        print(processed_data)
        processed_data_ = model.scale(processed_data)

        prediction, probabilities = model.prediction(processed_data_)
        print(data, prediction, probabilities)

        pipeline.producer_send(producer_t, 
            {'prediction': str(prediction),
            'proabilities_benign': str(probabilities[0][0]),
            'probabilities_malicious': str(probabilities[0][1]),
            'domain': data})