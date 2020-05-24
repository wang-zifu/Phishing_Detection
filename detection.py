from kafka import KafkaProducer, KafkaConsumer
import json 

class Detection:
    def __init__(self, server):
        self.__server = server

    def SetProducer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=self.__server,
            value_serializer=lambda values: json.dumps(values).encode('utf-8'))
        
    def kafkaSend(self, topic, data):
        self.producer.send(topic, data)

    def GetConsumer(self, topic, groupID):
        consumer = KafkaConsumer(topic, groupID)
        return consumer