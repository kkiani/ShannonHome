from packages.frameworks.connection import SHConnectionConsumer
import logging

logging.basicConfig(filename='shannon.log',level=logging.DEBUG)

class SensorConnection(SHConnectionConsumer):
    # public:
    is_motion_sensing = False
    temperature = 0.0
    delegate = None

    # private:
    __exchange_name = "com.shannon.sensor.motion"

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


class SensorConnectionDelegate:
    def motion_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')
    
    def temperature_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')