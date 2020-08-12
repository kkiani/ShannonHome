from packages.services.hws.hardware_requests import SHHardwareRequets
from packages.services.sensor.sensor_service import SensorService, SensorServiceDelegate
import time

class Services(SensorServiceDelegate):
    # public:
    # private:
    __hardware = SHHardwareRequets()
    __sensors = SensorService()

    def __init__(self):
        self.__sensors.delegate = self
        self.__sensors.start()
    
    def lamp(self, is_on: bool):
        self.__sensors.is_auto_light = False
        self.__hardware.lamp(isOn=is_on)
    
    def door(self):
        self.__hardware.door(isLock=False)
        time.sleep(1.0)
        self.__hardware.door(isLock=True)

    def auto_light(self, is_on: bool):
        self.__sensors.is_auto_light = is_on

    # SensorService Delegate:
    def is_lamp_on(self):
        return self.__hardware.is_lamp_on

    def set_lamp(self, on: bool):
        self.__hardware.lamp(isOn=on)