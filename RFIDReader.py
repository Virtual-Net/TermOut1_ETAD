#!/usr/bin/env python
#import serial
import RPi.GPIO as GPIO
from Logger_setup import logger
import json
from GeneralOutput import GeneralOutput
from pn532 import *

class RFIDReader(object):
    #serialrf = serial.Serial(
        #port='/dev/ttyUSB0',
        #baudrate=9600,
        #parity=serial.PARITY_NONE,
        #stopbits=serial.STOPBITS_ONE,
        #bytesize=serial.EIGHTBITS,
        #timeout=1
    #)

    #def __init__(self):
        #with open('/home/pi/AutoPark2020/TerminalEntranceSettings.json') as json_file:
            #data = json.load(json_file)
            #logging_file = data['logging_file']
        #logging.basicConfig(filename=logging_file, level=logging.INFO)
        # RS-232 configuration for rfid reader MultiISO 1.2.5
        #self.serialrfid = serial.Serial(
            #port='/dev/ttyUSB0',
            #baudrate=9600,
            #parity=serial.PARITY_NONE,
            #stopbits=serial.STOPBITS_ONE,
            #bytesize=serial.EIGHTBITS,
            #timeout=1
        #)

    #def bootrf(self, serialrf=None):
        #self.serialrf.write(str.encode('X'))
        #return None

    def readrf(self):
        try:
            pn532 = PN532_UART(debug=False, reset=20)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
            
            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
    
            print('Waiting for RFID/NFC card...')
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            #print('.', end="")
            # Try again if a no card is available.
            if uid is None:
                return
            else:
                print('Found card with UID:', [hex(i) for i in uid])
                logger.info(uid)
                uid_ = uid.hex()
                logger.info(uid_)
                return uid_
            #GPIO.cleanup()
        except:
            logger.info('RFID FAILED')
            pass

    #def readrf(self):
        #cardid = self.serialrf.readline()
        #cardid = cardid[:-2]
        #cardid = cardid.decode()
        #if cardid == 'N':
            #print('No RFID tag in range')
            #logging.info('No RFID tag in range')
            #return 0
        #elif cardid == 'S':
            #print(cardid)
            #self.bootrf()
            #return 0
        #elif cardid == 'MultiISO 1.2.5':
            #print(cardid)
            #self.singlerfreading()
            #return 0
        #elif cardid == '':
            #return 0
        #else:
            #buzzer = GeneralOutput()
            #buzzer.setbuzzerpin(0.1)
            #buzzer.resetbuzzerpin()
            #print('RFID card is: ' + cardid)
            #logging.info('RFID card is: ' + cardid)
            #return cardid

