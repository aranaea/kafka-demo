from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
import logging
import json
import os
import time

topic = os.environ.get('PCDEMO_CHANNEL') or 'stats'


class ConnectionException(Exception):
    pass


class Reader:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.debug("Initializing the consumer")
        while not hasattr(self, 'consumer'):
            self.logger.debug("Getting the kafka consumer")
            try:
                self.consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                                              consumer_timeout_ms=10,
                                              auto_offset_reset='earliest',
                                              group_id=None)
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: {0}".format(err))
                time.sleep(1)

        self.logger.debug("We have a consumer {0}".format(time.time()))
        self.consumer.subscribe(topic)
        # Wait for the topic creation and seek back to the beginning
        self.consumer.poll(timeout_ms=10000)
        self.consumer.seek(TopicPartition(topic, 0), 0)
        self.logger.debug("ok {0}".format(time.time()))

    def next(self):
        self.logger.debug("Reading stream: {0}".format(topic))
        try:
            if self.consumer:
                self.logger.debug("We have a consumer, calling 'next'")
                try:
                    event = self.consumer.next()
                    return json.loads(event.value)
                except StopIteration:
                    return None
            raise ConnectionException
        except AttributeError:
            self.logger.error("Unable to retrieve the next message.  "
                              "There is no consumer to read from.")
            raise ConnectionException


