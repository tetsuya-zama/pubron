#coding:utf-8
import json
import subprocess
import re
import logging

try:
    from shlex import quote
except ImportError:
    from pipes import quote


class Executor:
    """Executor

    This reads setting from 'executor.json'
    This executes defined shell commands when it recieved defined message.
    You can update 'executor.json' even if Pubron is running.
    """
    def __init__(self, setting_file_path):
        self.__setting_file_path = setting_file_path
        self.__logger = logging.getLogger("pubron.executor.Executor")

    def execute(self,msg):
        """Execute command defined on 'executor.json'.

        Args:
          msg : massage which subscriber recieved as Dictionary
            {
              msg:${name of message as String}
              data:${data for retrieve to command as Dictionary}
            }
        """
        with open(self.__setting_file_path,"r") as f:
            settings = json.load(f)

        self.__logger.debug(json.dumps(settings))
        for setting in settings :
            if msg.get("msg","") == setting["msg"] :
                self.__logger.info("msg[%s] matched",setting["msg"])
                self.__execute_command(setting["cmd"],msg.get("data",{}))

    def __execute_command(self,cmd,data):
        retrieved_cmd = self.__retrieve_data(cmd,data)
        self.__logger.info("execute command '%s'" , retrieved_cmd)
        subprocess.call(retrieved_cmd,shell=True)

    def __retrieve_data(self,cmd,data):
        result = cmd

        placeHolder_pattern = re.compile(r"##\S+##")
        placeHolders = re.findall(placeHolder_pattern,cmd)
        self.__logger.debug(placeHolders)

        variable_pattern = re.compile(r"##(\S+)##")
        for placeHolder in placeHolders :
            variable = re.search(variable_pattern,placeHolder).group(1)
            self.__logger.debug(variable)
            if variable == "DATA" :
                result = result.replace("##DATA##", quote(json.dumps(data)))
            elif data.has_key(variable) :
                result = result.replace("##" + variable + "##", quote(data[variable]))


        return result
