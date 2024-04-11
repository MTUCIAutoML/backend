import logging

from kafka.errors import NoBrokersAvailable

from settings import settings
import pickle
from kafka import KafkaProducer, KafkaConsumer, KafkaClient

from schemas.pv_interface import Arguments, ActionCommand, OutputSwitchCommand, PsCommand, State


class ActionError(Exception):
    pass


class KafkaManager:
    def __init__(self):
        self.con = settings.KAFKA_URL

        try:
            self.producer = KafkaProducer(bootstrap_servers=[self.con], api_version=(0,11,5),)
            self.consumer = KafkaConsumer("rtsp-response", bootstrap_servers=[self.con],
                                          reconnect_backoff_ms=1, consumer_timeout_ms=1000.0, api_version=(0,11,5))

            self.client = KafkaClient(bootstrap_servers=[self.con])
        except NoBrokersAvailable as err:
            logging.INFO(err)

    def action(self, rtsp_host, user, password, source_id, action):
        arguments = Arguments(rtsp_host, user, password)
        message = ActionCommand(cmd_id='rest', source_id=source_id, action=action, args=arguments)
        while True:
            self.producer.send('rtsp', pickle.dumps(message, protocol=5))
            self.producer.flush()
            response = next(self.consumer, None)

            if response:
                print(response.value)
                response = pickle.loads(response.value)
                break
        if response.successful is False:
            raise ActionError(response.message)
        return response.successful


kafkaManager = KafkaManager()



