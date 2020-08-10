
# ----- wrtie
from bluepy.btle import *

p = Peripheral()
address = '00:15:87:10:9A:4E'
p.connect(address, ADDR_TYPE_PUBLIC)
s = p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
c = s.getCharacteristics()[0]
c.write(bytes('fap', 'utf-8'))
p.disconnect()

# ---- reading
import binascii
import struct
import time
from bluepy import btle
import binascii

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(type(data))
        print(binascii.hexlify(data))
        print("A notification was received: %s" %data)


p = btle.Peripheral()
address = '00:15:87:10:9A:4E'
p.connect(address, btle.ADDR_TYPE_PUBLIC)


p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
ch = svc.getCharacteristics()[0]
print(ch.valHandle)

#p.writeCharacteristic(ch.valHandle+1, "\x02\x00")

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print("Waiting...")