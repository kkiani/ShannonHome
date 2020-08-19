from packages.services.hws.hardware_requests import SHHardwareRequets
from packages.services.push.push import SHPushService
from packages.services.sensor.sensor_connection import SensorConnection, SensorConnectionDelegate
from packages.services.security.security_connection import SecurityConnection, SecurityEvent
import time

class Services(SensorConnectionDelegate):
    # public:
    push = SHPushService()
    is_auto_light = False

    # private:
    __hardware = SHHardwareRequets()
    __sensors = SensorConnection()
    __security = SecurityConnection()
    __motion_last_sensing = int(time.time())
    __MOTION_DELAY = 1 * 60

    def __init__(self):
        self.__sensors.delegate = self
        self.__sensors.start()
    
    def lamp(self, is_on: bool):
        self.is_auto_light = False
        self.__hardware.lamp(isOn=is_on)
    
    def door(self):
        self.__hardware.door(isLock=False)
        time.sleep(1.0)
        self.__hardware.door(isLock=True)

    def security(self, is_on: bool):
        if is_on:
            self.__security.send_event(SecurityEvent.SECURITY_ON)
        else:
            self.__security.send_event(SecurityEvent.SECURITY_OFF)

    # Sensor Connection Delegate:
    def motion_did_update(self):
        if self.is_auto_light == False:
            return
        
        current_time = int(time.time())
        is_delay_pass = (self.__motion_last_sensing + self.__MOTION_DELAY < current_time)

        if self.__sensors.is_motion_sensing:
            self.__hardware.lamp(isOn=True)
        elif self.__hardware.is_lamp_on and (not is_delay_pass):
            self.__hardware.lamp(isOn=True)
        else:
            self.__hardware.lamp(isOn=False)

        if  self.__hardware.is_lamp_on and self.__sensors.is_motion_sensing:
            self.__motion_last_sensing = current_time

    def temperature_did_update(self):
        pass