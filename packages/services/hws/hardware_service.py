#!/usr/bin/env python
import pika
import serial


arduino_address = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_854333332313515052D0-if00"
arduino_serial_connection = serial.Serial(arduino_address, 9600, timeout=0.5)

# Create a global channel variable to hold our channel object in
channel = None

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_open_callback=on_channel_open)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume('test', handle_delivery)

# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
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

# Step #1: Connect to RabbitMQ using the default parameters
parameters = pika.ConnectionParameters()
connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()