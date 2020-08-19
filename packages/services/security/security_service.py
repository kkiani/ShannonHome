from packages.frameworks.service import SHServiceConsumer
from packages.services.security.security_events import SecurityEvent
from packages.services.push.push import SHPushService
import logging
import time

class SecurityService(SHServiceConsumer):
    def __init__(self, *args, **kwargs):
        super(SecurityService, self).__init__(*args, **kwargs)
        
        # public:
        self.is_enable = False

        # privete:
        self._push = SHPushService()
        self._exchange_name = 'com.shannon.security'
        self.__BREAK_IN_DELAY = 2 * 60
        self.__last_break_in = int(time.time()) - self.__BREAK_IN_DELAY

    def callback_func(self, channel, method, properties, body):
        message = body.decode("utf-8")
        if message == SecurityEvent.MOTION_SENSE.value:
            if self.is_enable:
                self.handle_break_in()
        elif message == SecurityEvent.LOGIN_FAIL_ATTEMPT.value:
            self.handle_failed_login()
        elif message == SecurityEvent.BAD_TOKEN_ATTEMPT.value:
            self.handle_failed_token()
        elif message == SecurityEvent.SECURITY_OFF.value:
            self.is_enable = False
            self._push.send_message('Security alert', 'System security service is turned off')
        elif message == SecurityEvent.SECURITY_ON.value:
            self.is_enable = True
            self._push.send_message('Security alert', 'System security service is turned on')
        else:
            self.handle_unkown_event(message)
    
    # event handlers
    def handle_break_in(self):
        current_time = int(time.time())
        if current_time > (self.__last_break_in + self.__BREAK_IN_DELAY):
            self._push.send_message('Security alert', 'someone is in your room.')
            self.__last_break_in = current_time

    def handle_failed_token(self):
        self._push.send_message('Security alert', 'a failed attempt with broken token to chenge system controls happend.')

    def handle_failed_login(self):
        self._push.send_message('Security alert', 'a failed login attempt has been occurred.')

    def handle_unkown_event(self, event_message):
        self._push.send_message('Security alert', 'System recived an unkown security event.')
        logging.warning('SecurityService: Unkown Event: {}'.format(event_message))

security = SecurityService()
security.start()