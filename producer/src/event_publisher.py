from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import os

topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'

class Publisher:

    def __init__(self, logger):
        self.logger = logger
        try:
            self.producer = KafkaProducer(bootstrap_servers="kafka:9092", api_version=(0,10))
        except NoBrokersAvailable as err:
            self.logger.error("Unable to find a broker: {0}".format(err))

    def push(self, message):
        self.logger.debug("Publishing: {0}".format(message))
        if self.producer:
            self.producer.send(topic, json.dumps(message))



