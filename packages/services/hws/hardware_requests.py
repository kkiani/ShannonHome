import pika

class SHHardwareRequets:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    def __init__(self):
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.queue_declare(queue='com.shannon.hws')

    def lamp(self, isOn: bool):
        if isOn:
            self.rabbitmq_channel.basic_publish(exchange='', routing_key='com.shannon.hws', body='lamp on')
        else:
            self.rabbitmq_channel.basic_publish(exchange='', routing_key='com.shannon.hws', body='lamp off')

    def door(self, isLock: bool):
        if isLock:
            self.rabbitmq_channel.basic_publish(exchange='', routing_key='com.shannon.hws', body='door lock')
        else:
            self.rabbitmq_channel.basic_publish(exchange='', routing_key='com.shannon.hws', body='door unlock')
    
    def __del__(self):
        self.rabbitmq_channel.close()
        self.rabbitmq_connection.close()