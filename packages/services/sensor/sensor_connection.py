from packages.frameworks.connection import SHConnectionConsumer


class SensorConnection(SHConnectionConsumer):
    # public:
    is_motion_sensing = False
    temperature = 0.0
    delegate = None

    # private:

    def callback_func(self, channel, method, properties, body):
        if body.decode("utf-8") == 'sensing':
            self.is_motion_sensing = True
            self.delegate.motion_did_update()
        elif  body.decode("utf-8")  == 'not sensing':
            self.is_motion_sensing = False
            self.motion_did_update()
        else:
            print(type(body))


class SensorConnectionDelegate:
    def motion_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')
    
    def temperature_did_update(self):
        raise Exception('Sensor Service Delegate not implemented.')