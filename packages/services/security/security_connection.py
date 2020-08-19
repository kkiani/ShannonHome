from packages.frameworks.connection import SHConnectionProducer
from packages.services.security.security_events import SecurityEvent


class SecurityConnection(SHConnectionProducer):
    def send_event(self, event: SecurityEvent):
        self.send(event.value)