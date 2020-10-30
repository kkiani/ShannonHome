import bluepy.btle as btle

class SHBLEDevice:
    address = None

    def __init__(self, address: str):
        self.address = address
    
    def connect(self):
        self.__connection = btle.Peripheral(self.address)
        self.__service = self.__connection.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
        self.__characteristic = self.__service.getCharacteristics()[0]

    def disconnect(self):
        self.__connection.disconnect()

    def send_code(self, code: bytes):
        self.__characteristic.write(code)

    def __del__(self):
        self.disconnect()