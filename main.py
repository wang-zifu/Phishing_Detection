from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
from detection.machine_learning import Model
import pandas as pd
import logging

def main():
    # LogConfig.set_logging_config('detection.log')
    server = "localhost:9092"

    # pipeline = DataPipe(server)
    # pipeline.set_producer()
    # pipeline.producer_send('test', {'test': 'hello'})

    # consumer = pipeline.get_consumer('test', 'test')
    # for msg in consumer:
    #     print(msg.value.decode())
    
    # Load a trained machine learning model 
    level_one_model = Model(model_name='./detection/models/layer_one_model').read_model()

    # Data
    data = 'hi.google2.com'

    # Level One Feature Extraction
    pre_processing = PreProcessing(data)
    pre_processed_data_DF = pre_processing.extraction()
    
    if not isinstance(pre_processed_data_DF, pd.DataFrame):
        logging.warning("Error Processing Observations.")
    print(pre_processed_data_DF)
    
    # Scale the data for machine learning 
    scaled_processed_data = pre_processing.scale_observations(pre_processed_data_DF)
    
    # Layer One Predictions
    level_1_predictions, probabilities = layer_one_model.prediction(scaled_processed_data[[
            'domain_length', 
            'percentage_numeric', 
            'top_level_domain_length', 
            'second_level_domain_length', 
            'num_dots', 'top_level_domain']])



if __name__ == "__main__":
    main()
    
