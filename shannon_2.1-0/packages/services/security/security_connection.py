from packages.frameworks.connection import SHConnectionProducer
from packages.services.security.security_events import SecurityEvent


class SecurityConnection(SHConnectionProducer):

    def __init__(self, *args, **kwargs):
        super(SecurityConnection, self).__init__(*args, **kwargs)

        # private:
        self._exchange_name = 'com.shannon.security'

    def send_event(self, event: SecurityEvent):
        self.send(event.value)