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
    layer_one_model = Model(layer=1, model_name='./detection/models/layer_one_model')
    if layer_one_model.read_model() == 0:
        logging.warning('Training a model')
        layer_one_model.train_controller()
    
    # Data
    data = 'google.com'

    # Level One Feature Extraction
    pre_processing = PreProcessing(data)
    processed_data = pre_processing.extraction()
    if not isinstance(processed_data, pd.DataFrame):
        logging.warning("Error Processing Observations.")
    
    processed_data_ = layer_one_model.scale(processed_data)
    print(processed_data_)
    # Layer One Predictions
    level_1_predictions, probabilities = layer_one_model.prediction(processed_data_)
    print(level_1_predictions, probabilities)

    from sklearn.metrics import classification_report,confusion_matrix
    from sklearn import metrics
    test_pred, proabilities = layer_one_model.prediction(layer_one_model.scale(layer_one_model.X_test))
    print(confusion_matrix(layer_one_model.Y_test,test_pred))
    print("Accuracy: %.2f" % (metrics.accuracy_score(layer_one_model.Y_test, test_pred)))
    print("Precision: %.2f" % (metrics.precision_score(layer_one_model.Y_test, test_pred)))
    print("Recall: %.2f" % (metrics.recall_score(layer_one_model.Y_test, test_pred)))
    print("F1-Score: %.2f" % (metrics.f1_score(layer_one_model.Y_test, test_pred)))


if __name__ == "__main__":
    main()
    
