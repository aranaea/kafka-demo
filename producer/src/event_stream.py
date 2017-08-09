from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json

class Stream:

    def __init__(self, logger):
        self.logger = logger
        try:
            self.producer = KafkaProducer(bootstrap_servers="kafka:9092", api_version=(0,10))
        except NoBrokersAvailable as err:
            self.logger.error("Unable to find a broker: {0}".format(err))

    def publish(self, message):
        self.logger.debug("Publishing: {0}".format(message))
        if self.producer:
            self.producer.send('stats', json.dumps(message))



