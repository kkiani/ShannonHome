import pika
import threading
import binascii
import time
from packages.services.hws.hardware_requests import SHHardwareRequets

class SensorService(threading.Thread):

    # public:
    is_motion_sensing = False
    is_auto_light_on = False
    temperature = 0.0

    # privates
    __exchange_name = "com.shannon.sensor.motion"
    __hardware_service = SHHardwareRequets()

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
            if self.is_auto_light_on:
                self.__hardware_service.lamp(isOn=True)
            self.is_motion_sensing = True
        elif  body.decode("utf-8")  == 'not sensing':
            if self.is_auto_light_on:
                self.__hardware_service.lamp(isOn=False)
            self.is_motion_sensing = False
        else:
            print(type(body))

