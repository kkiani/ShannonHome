import threading
import pika
import configparser

class SHServiceConsumer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(SHServiceConsumer, self).__init__(*args, **kwargs)

        # public:
        self.config = configparser.ConfigParser()

        # private:
        self._exchange_name = "com.shannon.framework.service"
        self.config.read('/etc/shannon.conf')

    def run(self):
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.exchange_declare(exchange=self._exchange_name, exchange_type='fanout')
        result = self.rabbitmq_channel.queue_declare(exclusive=True, queue='', arguments={'x-max-length': 1})
        self.rabbitmq_channel.queue_bind(result.method.queue, exchange=self._exchange_name)
        self.rabbitmq_channel.basic_consume(on_message_callback=self.callback_func, queue=result.method.queue)
        self.rabbitmq_channel.start_consuming()

    def terminate(self):
        self.rabbitmq_channel.stop_consuming()
    
    def callback_func(self, channel, method, properties, body):
        raise Exception('callback_func did not implemented.')


class SHServiceProducer(threading.Thread):
    pass