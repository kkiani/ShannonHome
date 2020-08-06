from ble_device import SHBLEDevice

class SHSwitchDevice(SHBLEDevice):
    def lamp(self, isOn: bool):
        if isOn:
            self.send_code(0x61)
        else:
            self.send_code(0x62)
    
    def door(self, isLock: bool):
        if isLock:
            self.send_code(0x72)
        else:
            self.send_code(0x71)
