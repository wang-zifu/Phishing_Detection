from kafka import KafkaProducer, KafkaConsumer
import json
import logging

class DataPipe:
    def __init__(self, server="localhost:9092"):
        """ Initialise a detection 
        Args:
            server (string): The IP address and port of the Kafka Broker
                the object will connect to.
        """
        self.__server = server

    def set_producer(self):
        """ Initalise a Kafka producer """
        self.producer = KafkaProducer(
            bootstrap_servers=self.__server,
            value_serializer=lambda values: json.dumps(values).encode('utf-8'))
        logging.warning('Producer Initialised.')

    def producer_send(self, topic, data):
        """ Send data to a Kafka Topic """
        self.producer.send(topic, data)

    def get_consumer(self, topic, groupID):
        """ Consume data from a Kafka Topic """
        consumer = KafkaConsumer(topic, 
            group_id=groupID)
        return consumer

    def get_consumer_json(self, topic, groupID):
        """ Consume data from a Kafka Topic """
        consumer = KafkaConsumer(topic, 
            group_id=groupID, 
            value_deserializer=lambda values: json.loads(values.decode('utf-8')))
        return consumer