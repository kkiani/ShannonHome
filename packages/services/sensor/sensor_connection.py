from packages.frameworks.connection import SHConnectionConsumer
import pika
import logging

logging.basicConfig(filename='shannon.log',level=logging.DEBUG)

class SensorConnection(SHConnectionConsumer):
    def __init__(self, *args, **kwargs):
        super(SensorConnection, self).__init__(*args, **kwargs)

        # public:
        self.is_motion_sensing = False
        self.temperature = 0.0
        self.delegate = None
        
        # private:
        self._exchange_name = "com.shannon.sensor.motion"

    def callback_func(self, channel, method, properties, body):
        try:
            if body.decode("utf-8") == 'sensing':
                self.is_motion_sensing = True
                self.delegate.motion_did_update()
            elif  body.decode("utf-8")  == 'not sensing':
                self.is_motion_sensing = False
                self.delegate.motion_did_update()
            else:
                print(type(body))
        except Exception as error:
            logging.error(str(error))

        channel.basic_ack(method.delivery_tag)


class SensorConnectionDelegate:
    def motion_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')
    
    def temperature_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')