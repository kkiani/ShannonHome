import time
from bluepy import btle
import binascii
import pika
import threading
import logging

class SensorBroadcaster(btle.DefaultDelegate):
    def __init__(self):
        self.__EXCHANGE_NAME = "com.shannon.sensor.motion"
        self.__motion_data_collector = self.__generate_data_collector('motion')
        btle.DefaultDelegate.__init__(self)
    
    def __generate_data_collector(self, name):
        logger = logging.getLogger('{}.{}'.format('com.shannon.sensor', name))
        log_formatter = logging.Formatter('%(asctime)s:%(message)s')
        file_handler = logging.FileHandler(name, mode='w')
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        return logger


    def send(self, message):
        self.connect()
        self.rabbitmq_channel.basic_publish(exchange=self.__EXCHANGE_NAME, routing_key='', body=message)
        self.disconnect()

    def connect(self):
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.exchange_declare(exchange=self.__EXCHANGE_NAME, exchange_type='fanout', arguments={'x-max-length': 10})

    def disconnect(self):
        self.rabbitmq_channel.close()
        self.rabbitmq_connection.close()

    def handleNotification(self, cHandle, data):
        status_code = binascii.hexlify(data)
        if status_code == b'30':
            self.send('sensing')
            self.__motion_data_collector.info('True')
        elif status_code == b'31':
            self.send('not sensing')
            self.__motion_data_collector.info('False')
        else:
            print(status_code)

class SensorDriver(threading.Thread):
    address = '00:15:87:10:9A:4E'
    broadcaster = SensorBroadcaster()

    def connect(self):
        print('[*] start connection to sensor bluetooth device.')
        self.p = btle.Peripheral()
        self.p.connect(self.address, btle.ADDR_TYPE_PUBLIC)
        self.p.setDelegate(self.broadcaster)
        self.svc = self.p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
        self.ch = self.svc.getCharacteristics()[0]

    def run(self):
        while True:
            if self.p.waitForNotifications(1.0):
                continue

    def disconnect(self):
        self.p.disconnect()

    def __send(self, message):
        self.broadcaster.send(message)



driver = SensorDriver()
driver.connect()
driver.start()
