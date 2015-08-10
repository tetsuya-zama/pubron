#coding:utf-8
"""Pubron

This is shell command kicker by subscribing pub-sub message.
This is compatible with Redis and PubNub for now.

Two setting json files(executor.json, subscriber.json) are required.

"executor.json" for defining commands to be kicked.
"subscriber.json" for defining subscriber of pub-sub messages.
"""

import os
from subscriber import subscriber
from executor import executor
import logging

if __name__ == "__main__":
    logger = logging.getLogger("pubron")
    fh = logging.FileHandler('pubron.log', 'a+')
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.setLevel(logging.INFO)

    executor_setting_file_path = os.path.join(os.path.dirname(__file__), 'executor.json')
    subscriber_setting_file_path = os.path.join(os.path.dirname(__file__), 'subscriber.json')

    executor = executor.Executor(executor_setting_file_path)
    subscriber.start(subscriber_setting_file_path,executor)
