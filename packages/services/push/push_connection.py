from pushover import init, Client
import configparser

class PushConnection():
    def __init__(self):
        # public:
        self.config = configparser.ConfigParser()
        self.config.read('/etc/shannon.conf')
        self.token = self.config["PUSH"]["Token"]
        self.user_id = self.config["PUSH"]["UserId"]

        # private:
        self.__client = Client(self.user_id, api_token=self.token)

    def send_message(self, title: str, message: str):
        self.__client.send_message(title, message)