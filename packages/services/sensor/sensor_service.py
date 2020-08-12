import pika
import threading
import binascii
import time
from packages.services.hws.hardware_requests import SHHardwareRequets

class SensorService(threading.Thread):
    # public:
    is_motion_sensing = False
    temperature = 0.0
    delegate = None

    # private:
    __exchange_name = "com.shannon.sensor.motion"
    __motion_last_update = int(time.time())
    __MOTION_DELAY = 10 * 60    # 10 miniutes
    __is_auto_light = False

    def __init__(self, *args, **kwargs):
        super(SensorService, self).__init__(*args, **kwargs)
    
    def run(self):
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.exchange_declare(exchange=self.__exchange_name, exchange_type='fanout')
        result = self.rabbitmq_channel.queue_declare(exclusive=True, queue='')
        self.rabbitmq_channel.queue_bind(result.method.queue, exchange=self.__exchange_name)
        self.rabbitmq_channel.basic_consume(on_message_callback=self.callback_func, queue=result.method.queue)
        self.rabbitmq_channel.start_consuming()

    def terminate(self):
        self.rabbitmq_channel.stop_consuming()
    
    def callback_func(self, channel, method, properties, body):
        if body.decode("utf-8") == 'sensing':
            self.is_motion_sensing = True
            self.motion_did_update()
        elif  body.decode("utf-8")  == 'not sensing':
            self.is_motion_sensing = False
            self.motion_did_update()
        else:
            print(type(body))

    def auto_light(self, is_on: bool):
        self.__is_auto_light = is_on
        self.__motion_last_update = int(time.time())

    def motion_did_update(self):
        if self.__is_auto_light == False:
            return

        current_time = int(time.time())

        if  self.delegate.is_lamp_on():
            self.__motion_last_update = current_time

        if self.__motion_last_update + self.__MOTION_DELAY < current_time:
            if self.delegate.is_lamp_on() != self.is_motion_sensing:
                self.delegate.set_lamp(on=self.is_motion_sensing)

    def temperature_did_update(self):
        pass
        

class SensorServiceDelegate:
    def is_lamp_on(self):
        raise Exception('Sensor Service Delegate not implemented.')

    def set_lamp(self, on: bool):
        raise Exception('Sensor Service Delegate not implemented.')
