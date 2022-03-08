import time
import serial
import automationhat
from Logger_setup import logger

class TicketDispenserPico(object):
	
    def __init__(self):
        self.ser = serial.Serial ("/dev/ttyS0", 115200, timeout=1)
        
	
    def resetticketdispenser(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x60\x01\x9B')
        logger.info('Ticket dispenser was reset')
	
    def getTicketDispenserStatus(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x23\x01\xC6')
        logger.info('Get Ticket Dispenser Sensors Status')

    def intaketochipcmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x49\x01\x88')
        logger.info('Send Ticket Dispenser Intake Cmd')
	
    def returnticketcmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x52\x01\x4F')
        logger.info('Send Ticket Dispenser Eject Cmd')
	
    def captureticketcmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x43\x01\x94')
        logger.info('Send Ticket Dispenser Capture Cmd')
	
    def readPosition2TicketDispenserCmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x32\x01\xAB')
        logger.info('Send Ticket Dispenser ReadPosition2 Cmd')
	
    def readPosition1TicketDispenserCmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x34\x01\xA9')
        logger.info('Send Ticket Dispenser ReadPosition1 Cmd')
	
    def readPosition3TicketDispenserCmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x36\x01\xA7')
        logger.info('Send Ticket Dispenser ReadPosition2 Cmd')
	
    def stepInTicketDispenserCmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x44\x01\x93')
        logger.info('Send Ticket Dispenser Step In Cmd')
	
    def stepOutTicketDispenserCmd(self):
        self.ser.write(b'\x01\x01\x01\x01\x00\x45\x01\x92')
        logger.info('Send Ticket Dispenser Step Out Cmd')
	
    def readTicketDispenserResponse(self):
        # time.sleep(0.5)
        ticketDispenserStatus = 0
        try:
            ticketDispenserStatus = self.ser.read()
            # time.sleep(0.03)
            data_left = self.ser.inWaiting()
            ticketDispenserStatus += self.ser.read(data_left)
            print(ticketDispenserStatus)
        except:
            pass
        return ticketDispenserStatus





