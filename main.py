from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
from detection.machine_learning import Model
from detection.triage import Triage
import pandas as pd
import logging
import os 

def config_check():
    deployement_style = os.environ.get('MACHINE_TYPE')
    if deployement_style == 0:
        pass
    elif deployement_style == 1:
        pass
    elif deployement_style == 2:
        pass

def triage_deployement(server):
    # Consume Predictions
    core_decision_consumer = pipeline.get_consumer('test_core', 'test')
    # Make decision using default threshold [0.40, 0.60]
    triage = Triage()
    for data in core_decision_consumer:
        data = data.value.decode()
        decision = triage.decision_maker()
    # Produce
    pipeline = DataPipe(server)
    pipeline.set_producer()
    # Produce to layer_one_output
    # OR
    # Produce to layer_two_output
    pass

def main():
    # LogConfig.set_logging_config('detection.log')
    server = "localhost:9092"

    # Load a trained machine learning model 
    model = Model(layer=1, model_name='./detection/models/layer_one_model')
    if not model.read_model():
        logging.warning('Training a model')
        model.train_controller()
    
    # Initialise SEND 
    pipeline = DataPipe(server)
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
        


if __name__ == "__main__":
    main()
    
