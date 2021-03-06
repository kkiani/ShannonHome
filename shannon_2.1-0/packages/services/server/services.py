from packages.services.hws.hardware_requests import SHHardwareRequets
from packages.services.push.push_connection import PushConnection
from packages.services.sensor.sensor_connection import SensorConnection, SensorConnectionDelegate
from packages.services.security.security_connection import SecurityConnection, SecurityEvent
from packages.services.led_strip.led_connection import LEDConnection
import time
import configparser

class Services(SensorConnectionDelegate):
    def __init__(self):
        # public:
        self.push = PushConnection()
        self.is_auto_light = False
        self.hardware = SHHardwareRequets()
        self.sensors = SensorConnection()
        self.sensors.delegate = self
        self.sensors.start()
        self.security = SecurityConnection()
        self.config = configparser.ConfigParser()
        self.config.read('/etc/shannon.conf')
        self.led_strip = LEDConnection()

        # private:
        self.__motion_last_sensing = int(time.time())
        self.__MOTION_DELAY = int(self.config['SENSOR']['delay']) * 60

    
    def lamp(self, is_on: bool):
        self.is_auto_light = False
        self.hardware.lamp(isOn=is_on)
    
    def door(self):
        self.hardware.door(isLock=False)
        time.sleep(1.0)
        self.hardware.door(isLock=True)

    # Sensor Connection Delegate:
    def motion_did_update(self):
        if self.is_auto_light == False:
            return
        
        current_time = int(time.time())
        is_delay_pass = (self.__motion_last_sensing + self.__MOTION_DELAY < current_time)

        if self.sensors.is_motion_sensing:
            self.hardware.lamp(isOn=True)
        elif self.hardware.is_lamp_on and (not is_delay_pass):
            self.hardware.lamp(isOn=True)
        else:
            self.hardware.lamp(isOn=False)

        if  self.hardware.is_lamp_on and self.sensors.is_motion_sensing:
            self.__motion_last_sensing = current_time

    def temperature_did_update(self):
        pass