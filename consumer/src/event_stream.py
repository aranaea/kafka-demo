from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import os

topic = 'stats' # os.environ['DEMO_CHANNEL'] or 'stats'

class Stream():

    def __init__(self, logger):
        self.logger = logger
        try:
            self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092", api_version=(0, 10), consumer_timeout_ms=10)
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
                return { "status": "success", "message": "There are no events on the stream"} #TODO this should return an empty document
        return None



