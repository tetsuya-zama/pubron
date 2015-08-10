#coding:utf-8
import json
import redissubscriber
import pubnubsubscriber
__types = {"REDIS":"redis","PUBNUB":"pubnub",}

def start(setting_file_path,executor):
    """Start subscriber(s) definded on 'subscriber.json'.

    You may not update 'subscriber.json' while Pubron is running.

    Args:
      setting_file_path : file path for 'subscriber.json'
      executor : instance of executor.executor.Executor
    """
    with open(setting_file_path,"r") as f:
        settings = json.load(f)

    for setting in settings:
        if setting["type"] == __types["REDIS"] :
            redissubscriber.create(setting,executor)
        if setting["type"] == __types["PUBNUB"] :
            pubnubsubscriber.create(setting,executor)
