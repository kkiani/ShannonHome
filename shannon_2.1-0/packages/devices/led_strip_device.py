from ble_device import SHBLEDevice

class SHLEDStripDevice(SHBLEDevice):
    def turn_blue(self):
        self.send_code(0x61)
    
    def sturn_white(self):
        self.send_code(0x62)

    def turn_green(self):
        self.send_code(0x63)
    
    def turn_red(self):
        self.send_code(0x64)
    
    def turn_off(self):
        self.send_code(0x65)