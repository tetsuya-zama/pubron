#coding:utf-8
from redis import Redis
import threading
import json
import logging

def create(setting, executor):
    """Create and start Redis Subscriber

    Args:
      setting : one of subscriber settings on 'subscriber.json' as Dictionary
      executor : instance of executor.executor.Executor
    """
    RedisSubscriberThread(setting,executor).run()




class RedisSubscriberThread(threading.Thread):
    def __init__(self,setting,executor):
        super(RedisSubscriberThread, self).__init__()
        self.__setting = setting
        self.__executor = executor
        self.__logger = logging.getLogger("pubron.subscriber.RedisSubscriberThread")

    def run(self):
        if self.__setting.has_key("password"):
            conn = Redis(host=self.__setting["host"],port=self.__setting["port"],password=self.__setting["password"])
        else:
            conn = Redis(host=self.__setting["host"],port=self.__setting["port"],password=None)

        pubsub = conn.pubsub()
        pubsub.subscribe(self.__setting["channel"])

        self.__logger.info("redis subscriber start. setting:%s", json.dumps(self.__setting))

        for msg in pubsub.listen():
            if isinstance(msg["data"],str):
                try:
                    self.__executor.execute(json.loads(msg["data"]))
                    self.__logger.info("message recieved. %s",msg)
                except ValueError as e:
                    self.__logger.warn(str(e))
