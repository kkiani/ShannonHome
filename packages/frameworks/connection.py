import threading
import pika
import configparser

class SHConnectionConsumer(threading.Thread):
    # public:
    config = configparser.ConfigParser()

    # private:
    __exchange_name = 'com.shannon.framework.connection'

    def __init__(self, *args, **kwargs):
        super(SHConnectionConsumer, self).__init__(*args, **kwargs)
        self.config.read('/etc/shannon.conf')

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
        raise Exception('callback_func did not implemented.')


class SHConnectionProducer:
    # public:
    # private:
    __exchange_name = 'com.shannon.framework.connection'

    # only to have same interface with SHConnectionConsumer
    def start(self):
        pass

    def send(self, message):
        self.connect()
        self.rabbitmq_channel.basic_publish(exchange=self.__exchange_name, routing_key='', body=message)
        self.disconnect()

    def connect(self):
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.exchange_declare(exchange=self.__exchange_name, exchange_type='fanout', arguments={'x-max-length': 10})

    def disconnect(self):
        self.rabbitmq_channel.close()
        self.rabbitmq_connection.close()