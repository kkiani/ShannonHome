import pika

class SHHardwareRequets:
    __lamp_on = True
    __door_lock = True

    @property
    def is_lamp_on(self):
        return self.__lamp_on
    
    @property
    def is_door_lock(self):
        return self.__door_lock

    def connect(self):
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()
        self.rabbitmq_channel.queue_declare(queue='com.shannon.hws')
        
    def disconnect(self):
        self.rabbitmq_channel.close()
        self.rabbitmq_connection.close()

    def send(self, message):
        self.connect()
        self.rabbitmq_channel.basic_publish(exchange='', routing_key='com.shannon.hws', body=message)
        self.disconnect()

    def lamp(self, isOn: bool):
        if self.is_lamp_on == isOn:
            return
            
        if isOn:
            self.send('lamp on')
        else:
            self.send('lamp off')

        self.__lamp_on = isOn

    def door(self, isLock: bool):
        if isLock:
            self.send('door lock')
        else:
            self.send('door unlock')

        self.__door_lock = isLock
    
    def __del__(self):
        self.disconnect()