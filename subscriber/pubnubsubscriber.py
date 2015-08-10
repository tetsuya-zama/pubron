#coding:utf-8
from pubnub import Pubnub
import json
import logging

def create(setting, executor):
    """Create and start PubNub Subscriber

    Args:
      setting : one of settings on 'subscriber.json' as Dictionary
      executor : instance of executor.executor.Executor
    """
    PubNubSubscriber(setting,executor).run()


class PubNubSubscriber:
    def __init__(self,setting,executor):
        self.__setting = setting
        self.__executor = executor
        self.__logger = logging.getLogger("pubron.subscriber.PubNubSubscriber")

    def __callback(self,message,channel):
        try:
            self.__executor.execute(json.loads(message))
            self.__logger.info("message recieved. %s", json.loads(message))
        except ValueError as e:
            self.__logger.warn(str(e))

    def run(self):
        pubnub = Pubnub(subscribe_key=self.__setting["sub-key"],publish_key=self.__setting["pub-key"])
        pubnub.subscribe(channels=self.__setting["channel"], callback=self.__callback)

        self.__logger.info("pubnub subscriber start. setting:%s", json.dumps(self.__setting))
