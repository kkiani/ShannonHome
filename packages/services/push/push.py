import http.client, urllib
from enum import Enum
import configparser

class SHPushMessagePriority(Enum):
    LOWEST = -2
    LOW = -1
    NORMAL = 0
    HIGH = 1


class SHPushService():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('/etc/shannon.conf')
        self.token = self.config["PUSH"]["Token"]
        self.user_id = self.config["PUSH"]["UserId"]
        self.__connection = http.client.HTTPSConnection("api.pushover.net:443")

    def send_message(self, title, message, url='', url_title='', priority=SHPushMessagePriority.NORMAL):
        self.__connection.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
            "token": self.token,
            "user": self.user_id,
            "title":title,
            "sound":"classical",
            "message": message,
            "url":url,
            "url_title":url_title,
            "priority":priority.value,
            }), { "Content-type": "application/x-www-form-urlencoded" })
        resp = self.__connection.getresponse()
        resp.read()

    def __del__(self):
        self.__connection.close() 
