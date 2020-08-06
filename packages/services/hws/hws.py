#!/usr/bin/python

appID = "hws-52b6ae947629ba03029087dda2390257"
# to find out Arduino device ID get ls in path /dev/serial/by-id
HardwareDeviceID = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_854333332313515052D0-if00"

import sys, time
# from daemon import *
# from Setting import dictSetting
import serial
import os

tempPath = sys.path
sys.path.append(os.path.expanduser('/system/shframework'))

from SHSetting import dictSetting
from SHLogger import logger
from SHDaemon import *

mainPath = os.path.expanduser('/system/bot')
tasksPath = mainPath + '/Tasks'

helpStr = """
Usage: hws <command> [<args>]

  stop				stop service
  start				start service
  restart			restart servcie

  door				open door lock
  temp				Room Temperature (LM35 sensor)

  lampOn			turn on lamp
  lampOff			turn oof lamp
  lampSwitch		switch lamp state

  speakerOn			turn on speakers
  speakerOff		turn off speakers
  speakerSwitch		switch speaker state

  AutoLightOn		Turn on automatic light control
  AutoLightOff		Turn off automatic light control
  AutoLightSwitch	Switch automatic light control

  mugOn				turn on mug
  mugOff			turn oof mug

  serialPush		send a message on serial port

  help				show this message

"""


class HardwareService(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)

        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.setting_path = '/stg/' + appID + '.json'
        self.setting = dictSetting(self.setting_path)
        self.setting.load()

    def run(self):
        while True:
            time.sleep(5)


def main():
    global helpStr
    global HardwareDeviceID

    ser = serial.Serial(HardwareDeviceID, 9600, timeout=0.5)
    hws = HardwareService('/pid/' + appID + '.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            hws.start()

        elif 'stop' == sys.argv[1]:
            hws.stop()

        elif 'restart' == sys.argv[1]:
            hws.restart()

        elif 'door' == sys.argv[1]:
            ser.write("4")
            time.sleep(1)
            ser.write("5")

        elif 'mugOn' == sys.argv[1]:
            ser.write("8")
            hws.setting.setKeyForValue('mug', True)

        elif 'mugOff' == sys.argv[1]:
            ser.write("9")
            hws.setting.setKeyForValue('mug', True)

        elif 'mugSwitch' == sys.argv[1]:
            if hws.setting.valueForKey('mug') == True:
                ser.write("9")
                hws.setting.setKeyForValue('mug', False)
            else:
                ser.write("8")
                hws.setting.setKeyForValue('mug', True)

        elif 'lampOn' == sys.argv[1]:
            ser.write("3")
            hws.setting.setKeyForValue('lamp', True)

        elif 'lampOff' == sys.argv[1]:
            ser.write("2")
            hws.setting.setKeyForValue('lamp', False)

        elif 'lampSwitch' == sys.argv[1]:
            if hws.setting.valueForKey('lamp') == True:
                ser.write("2")
                hws.setting.setKeyForValue('lamp', False)
            else:
                ser.write("3")
                hws.setting.setKeyForValue('lamp', True)

        elif 'speakerSwitch' == sys.argv[1]:
            if hws.setting.valueForKey('speaker') == True:
                ser.write("7")
                hws.setting.setKeyForValue('speaker', False)
            else:
                ser.write("6")
                hws.setting.setKeyForValue('speaker', True)

        elif 'speakerOn' == sys.argv[1]:
            ser.write("6")
            hws.setting.setKeyForValue('speaker', True)

        elif 'speakerOff' == sys.argv[1]:
            ser.write("7")
            hws.setting.setKeyForValue('speaker', False)

        elif 'AutoLightOn' == sys.argv[1]:
            ser.write("ALOn")
            hws.setting.setKeyForValue('AL', True)

        elif 'AutoLightOff' == sys.argv[1]:
            ser.write("ALOff")
            hws.setting.setKeyForValue('AL', False)

        elif 'AutoLightSwitch' == sys.argv[1]:
            if hws.setting.valueForKey('AL') == True:
                ser.write("ALOff")
                hws.setting.setKeyForValue('AL', False)
            else:
                ser.write("ALOn")
                hws.setting.setKeyForValue('AL', True)

        elif 'temp' == sys.argv[1]:
            ser.write("temp")
            time.sleep(1)
            resp = ser.read(ser.inWaiting())
            print(resp)

        elif 'motion' == sys.argv[1]:
            ser.write("motion")
            time.sleep(1)
            resp = ser.read(ser.inWaiting())
            print(resp)

        elif 'help' == sys.argv[1]:
            print(helpStr)
            sys.exit(2)

        elif 'serialPush' == sys.argv[1]:
            message = sys.argv[2]
            ser.write(message)

        else:
            print('Unknown commamd')
            sys.exit(2)
            hws.restart()
        sys.exit(0)
    else:

        print(helpStr)
        sys.exit(2)


if __name__ == '__main__':
    main()
