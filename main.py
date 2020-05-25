from detection.data_pipe import DataPipe
from processing.pre_processing import PreProcessing
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
    
    # Data
    data = 'hi.google2.com'

    # Level One Feature Extraction
    pre_processing = PreProcessing(data)
    pre_processed_data_DF = pre_processing.extraction()
    
    if not isinstance(pre_processed_data_DF, pd.DataFrame):
        logging.warning("Error Processing Observations.")
    print(pre_processed_data_DF)

if __name__ == "__main__":
    main()
    
