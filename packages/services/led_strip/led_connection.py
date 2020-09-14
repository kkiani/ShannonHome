from packages.frameworks.connection import SHConnectionProducer

class LEDConnection(SHConnectionProducer):
    def __init__(self, *args, **kwargs):
        super(LEDConnection, self).__init__(*args, **kwargs)

        self._exchange_name = 'com.shannon.led_strip'

    def turn_green(self):
        self.send('green')

    def turn_blue(self):
        self.send('blue')
    
    def turn_red(self):
        self.send('red')

    def turn_off(self):
        self.send('off')