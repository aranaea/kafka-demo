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
        """
        Get the "next" event.  This is a pretty naive implementation.  It
        doesn't try to deal with multiple partitions or anything and it assumes
        the event payload is json.
        :return: The event in json form
        """
        self.logger.debug("Reading stream: {0}".format(topic))
        try:
            if self.consumer:
                self.logger.debug("A consumer is calling 'next'")
                try:
                    # This would be cleaner using `next(consumer)` except
                    # that there is no timeout on that call.
                    event_partitions = self.consumer.poll(timeout_ms=100,
                                                          max_records=1)
                    event_list = list(event_partitions.values())
                    payload = event_list[0][0]
                    event = payload.value
                    self.logger.debug('Read an event from the stream {}'.
                                      format(event))
                    try:
                        return json.loads(event)
                    except json.decoder.JSONDecodeError:
                        return json.loads(f'{{ "message": "{event}" }}')
                except (StopIteration, IndexError):
                    return None
            raise ConnectionException
        except AttributeError as ae:
            self.logger.error("Unable to retrieve the next message.  "
                              "There is no consumer to read from.")
            self.logger.error(str(ae))
            raise ConnectionException
