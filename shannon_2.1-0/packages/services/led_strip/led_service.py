from bluepy import btle
from packages.frameworks.service import SHServiceConsumer
from packages.services.push.push_connection import PushConnection

class LEDService(SHServiceConsumer):
    def __init__(self, *args, **kwargs):
        super(LEDService, self).__init__(*args, **kwargs)
        
        self.__address = self.config['LED']['address']
        self._exchange_name = 'com.shannon.led_strip'

    def callback_func(self, channel, method, properties, body):
        message = body.decode("utf-8")
        if message == 'red':
            self.__write(bytes([0xfd]))
        elif message == 'green':
            self.__write(bytes([0xfe]))
        elif message == 'blue':
            self.__write(bytes([0xfc]))
        elif message == 'off':
            self.__write(bytes([0xff]))

    def connect(self):
        print('[*] start connection to sensor bluetooth device.')
        self.p = btle.Peripheral()
        self.p.connect(self.address, btle.ADDR_TYPE_PUBLIC)
        self.svc = self.p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
        self.ch = self.svc.getCharacteristics()[0]

    def __write(self, code):
        self.ch.write(code)