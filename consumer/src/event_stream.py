from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import os

topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'

class ConnectionException(Exception):
    pass

class Stream():

    def __init__(self, logger):
        self.logger = logger
        try:
            self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092", api_version=(0, 10), consumer_timeout_ms=100)
            self.consumer.subscribe(topic)
        except NoBrokersAvailable as err:
            self.logger.error("Unable to find a broker: {0}".format(err))

    def read_stream(self):
        self.logger.debug("Reading stream")
        if self.consumer:
            try:
                event = self.consumer.next()
                return json.loads(event.value)
            except StopIteration:
                return None
        raise ConnectionException



