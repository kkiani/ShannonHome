from packages.services.hws.hardware_requests import SHHardwareRequets
from packages.services.push.push import SHPushService
from packages.services.sensor.sensor_connection import SensorConnection, SensorConnectionDelegate
from packages.services.security.security_connection import SecurityConnection, SecurityEvent
import time

class Services(SensorConnectionDelegate):
    # public:
    push = SHPushService()
    is_auto_light = False
    hardware = SHHardwareRequets()
    sensors = SensorConnection()
    security = SecurityConnection()

    # private:
    __motion_last_sensing = int(time.time())
    __MOTION_DELAY = 1 * 60

    def __init__(self):
        self.sensors.delegate = self
        self.sensors.start()
    
    def lamp(self, is_on: bool):
        self.is_auto_light = False
        self.hardware.lamp(isOn=is_on)
    
    def door(self):
        self.hardware.door(isLock=False)
        time.sleep(1.0)
        self.hardware.door(isLock=True)

    # Sensor Connection Delegate:
    def motion_did_update(self):
        self.security.send_event(SecurityEvent.MOTION_SENSE)

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