#!/usr/bin/env python
import pika
import serial


arduino_address = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_854333332313515052D0-if00"
arduino_serial_connection = serial.Serial(arduino_address, 9600, timeout=0.5)

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
rabbitmq_channel = rabbitmq_connection.channel()

rabbitmq_channel.queue_declare(queue='com.shannon.hws')


def callback(ch, method, properties, body):
    if body == b'lamp off':
        arduino_serial_connection.write("2")
    elif body == b'lamp on':
        arduino_serial_connection.write("3")
    elif body == b'door lock':
        arduino_serial_connection.write("5")
    elif body == b'door unlock':
        arduino_serial_connection.write("4")
    else:
        print(' [!] unknown command: {}'.format(body))


rabbitmq_channel.basic_consume('com.shannon.hws', callback, True)

print(' [*] Waiting for messages. To exit press CTRL+C')
rabbitmq_channel.start_consuming()