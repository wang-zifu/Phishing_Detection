from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
from detection.machine_learning import Model
import pandas as pd
import logging

def main():
    # LogConfig.set_logging_config('detection.log')
    server = "localhost:9092"

    # Load a trained machine learning model 
    layer_one_model = Model(layer=1, model_name='./detection/models/layer_one_model')
    if not layer_one_model.read_model():
        logging.warning('Training a model')
        layer_one_model.train_controller()
    
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
            continue 
        processed_data_ = layer_one_model.scale(processed_data)

        # Layer One Predictions
        level_1_predictions, probabilities = layer_one_model.prediction(processed_data_)
        print(level_1_predictions, probabilities)

        pipeline.producer_send('test_y', {'prediction': str(level_1_predictions),
                                        'proabilities': str(probabilities),
                                        '_data': data})
        


if __name__ == "__main__":
    main()
    
