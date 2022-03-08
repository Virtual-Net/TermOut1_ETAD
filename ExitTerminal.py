#!/usr/bin/python
# coding=utf-8
import time
import queue
import signal
import threading
from tkinter import *
from dateutil.parser import parse
import sys
import select
# from inputimeout import inputimeout, TimeoutOccurred
# internal imports
from HttpManager import *
from RFIDReader import *
from GeneralInput import *
from TicketDispenserDDM import *
from TicketDispenserAdel import *
from TicketDispenserPico import *
# from USBBarcodeHandler import *
# from BarcodeHandler import *
# from Barcode import *
from Logger_setup import logger
from gpiozero import CPUTemperature
import json
import socket
import evdev
from evdev import InputDevice, categorize  # import * is evil :)

TIMEOUT = 0.1
messageflag = False
enabledispenser = False
IP_PORT = 7001
HOSTNAME = ""



class GuiPart:

    def __init__(self, master, queue, endCommand):
        self.queue = queue
        #try:
        self.GUI = Tk()
        self.master2 = master
        self.GUI.attributes('-fullscreen', True)
        self.GUI.config(bg="black")

        self.F1 = Frame(self.GUI)
        self.F1 = Frame(self.GUI, width=400, height=200)
        self.F1.place(height=500, width=400, x=100, y=100)
        self.F1.config()

        self.F1.grid(columnspan=10, rowspan=10)
        self.F1.grid_rowconfigure(0, weight=1)

        self.photo = PhotoImage(master=self.GUI, file="/home/pi/AutoPark2020_Exit/Images/DCS_2502.png")
        self.label = Label(self.GUI, image=self.photo, bg="black")
        self.label.image = self.photo  # keep a reference!
        self.label.grid(row=0, column=0, columnspan=20, rowspan=30)

        self.line1 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 28 bold")
        self.line1.grid(row=8, column=9)
        self.line2 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 26 bold")
        self.line2.grid(row=9, column=9)
        self.line3 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 26 bold")
        self.line3.grid(row=10, column=9)
        self.line4 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 28 bold")
        self.line4.grid(row=17, column=9)
        self.line5 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 26 bold")
        self.line5.grid(row=18, column=9)
        self.line6 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 26 bold")
        self.line6.grid(row=19, column=9)
        # Add more GUI stuff here depending on your specific needs
        """except:
            self.GUI = Tk()
            self.master2 = master
            #self.GUI.attributes('-fullscreen', True)

            self.F1 = Frame(self.GUI)
            self.F1 = Frame(self.GUI, width=400, height=200)
            self.F1.place(height=500, width=400, x=100, y=100)
            self.F1.config()

            self.F1.grid(columnspan=10, rowspan=10)
            self.F1.grid_rowconfigure(0, weight=1)

            self.photo = PhotoImage(master=self.GUI, file="/home/pi/AutoPark2020_optimization/Images/DCS_2502.png")
            self.label = Label(self.GUI, image=self.photo)
            self.label.image = self.photo  # keep a reference!
            self.label.grid(row=0, column=0, columnspan=20, rowspan=30)

            self.line1 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
            self.line1.grid(row=10, column=3)
            #self.line2 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
            #self.line2.grid(row=9, column=3)
            #self.line3 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
            #self.line3.grid(row=10, column=3)
            #self.line4 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 20 bold")
            #self.line4.grid(row=13, column=3)
            #self.line5 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
            #self.line5.grid(row=14, column=3)
            #self.line6 = Label(self.GUI, text="", bg="black", fg="white", font="Verdana 18 bold")
            #self.line6.grid(row=15, column=3)
            # Add more GUI stuff here depending on your specific needs"""


    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        #self.queue.put(1)
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                logger.info("incoming msg: {}".format(msg))
                #msg = msgc
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                #logger.info(msg)
                if msg == 1:
                    #logger.info('update messages')
                    self.line1['text'] = "WELCOME"
                    self.line2['text'] = "INSERT YOUR TICKET"
                    self.line3['text'] = "OR CARD"
                    self.line4['text'] = "ΚΑΛΩΣΗΡΘΑΤΕ"
                    self.line5['text'] = "ΕΙΣΑΓΕΤΕ ΤΟ ΕΙΣΙΤΗΡΙΟ"
                    self.line6['text'] = "Ή ΤΗΝ ΚΑΡΤΑ ΣΑΣ"
                    # self.master2.after(200, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(200, ThrededClient.periodicCall)
                    #print('msg update')
                if msg == 2:
                    #logger.info('update messages')
                    self.line1['text'] = ""
                    self.line2['text'] = ""
                    self.line3['text'] = ""
                    self.line4['text'] = ""
                    self.line5['text'] = ""
                    self.line6['text'] = ""
                    # self.master2.after(200, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(200, ThrededClient.periodicCall)
                if len(str(msg)) > 4:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "WAIT"
                    self.line3['text'] = ""
                    self.line4['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line5['text'] = "ΠΕΡΙΜΕΝΕΤΕ"
                    self.line6['text'] = ""
                    # self.master2.after(200, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(800, ThrededClient.periodicCall)
                if msg == 201 or msg == 200:
                    #logger.info('update messages')
                    self.line1['text'] = "VALID"
                    self.line2['text'] = "EXIT"
                    self.line3['text'] = "THANK YOU"
                    self.line4['text'] = "ΕΞΟΔΟΣ"
                    self.line5['text'] = "ΔΕΚΤΗ"
                    self.line6['text'] = "ΕΥΧΑΡΙΣΤΟΥΜΕ"
                    # self.master2.after(1000, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(1000, ThrededClient.periodicCall)
                if msg == 405:
                    #logger.info('update messages')
                    self.line1['text'] = "CARD"
                    self.line2['text'] = "NOT"
                    self.line3['text'] = "REGISTERED"
                    self.line4['text'] = "ΜΗ"
                    self.line5['text'] = "ΚΑΤΑΧΩΡΗΜΕΝΗ"
                    self.line6['text'] = "ΚΑΡΤΑ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
                if msg == 406:
                    #logger.info('update messages')
                    self.line1['text'] = "BOOKING"
                    self.line2['text'] = "NOT"
                    self.line3['text'] = "FOUND"
                    self.line4['text'] = "ΔΕΝ"
                    self.line5['text'] = "ΒΡΕΘΗΚΕ"
                    self.line6['text'] = "ΚΡΑΤΗΣΗ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
                if msg == 404:
                    #logger.info('update messages')
                    self.line1['text'] = "TICKET"
                    self.line2['text'] = "NOT"
                    self.line3['text'] = "FOUND"
                    self.line4['text'] = "ΔΕΝ"
                    self.line5['text'] = "ΒΡΕΘΗΚΕ"
                    self.line6['text'] = "ΕΙΣΙΤΗΡΙΟ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # ThreadedClient.root.after(4000, ThrededClient.periodicCall)
                if msg == 503:
                    #logger.info('update messages')
                    self.line1['text'] = "VEHICLE"
                    self.line2['text'] = "ALREADY"
                    self.line3['text'] = "EXITED"
                    self.line4['text'] = "ΤΟ ΟΧΗΜΑ"
                    self.line5['text'] = "ΕΧΕΙ ΗΔΗ"
                    self.line6['text'] = "ΕΞΕΛθΕΙ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
                if msg == 504:
                    #logger.info('update messages')
                    self.line1['text'] = "YOU"
                    self.line2['text'] = "MUST PAY"
                    self.line3['text'] = "BEFORE EXIT"
                    self.line4['text'] = "ΠΡΕΠΕΙ"
                    self.line5['text'] = "ΝΑ ΠΛΗΡΩΣΕΤΕ"
                    self.line6['text'] = "ΠΡΙΝ ΤΗΝ ΕΞΟΔΟ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
                if msg == 505:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "TRY"
                    self.line3['text'] = "AGAIN"
                    self.line4['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line5['text'] = "ΠΡΟΣΠΑΘΗΣΤΕ"
                    self.line6['text'] = "ΞΑΝΑ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
                if msg == 506:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "RETRIEVE"
                    self.line3['text'] = "YOUR TICKET"
                    self.line4['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line5['text'] = "ΠΑΡΑΛΑΒΕΤΕ"
                    self.line6['text'] = "ΤΟ ΕΙΣΙΤΗΡΙΟ ΣΑΣ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
                if msg == 507:
                    #logger.info('update messages')
                    self.line1['text'] = "PLEASE"
                    self.line2['text'] = "CONTACT"
                    self.line3['text'] = "THE CASHIER"
                    self.line4['text'] = "ΠΑΡΑΚΑΛΩ"
                    self.line5['text'] = "ΕΠΙΚΟΙΝΩΝΗΣΤΕ"
                    self.line6['text'] = "ΜΕ ΤΟ ΤΑΜΕΙΟ"
                    # self.master2.after(4000, ThreadedClient.periodicCall(self))
                    # threading.Timer(4, ThreadedClient.periodicCall).start()
                #print(self.queue)
            except:
                # self.master2.after(200, ThreadedClient.periodicCall)
                logger.info('QUEUE IS EMPTY')
                pass
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                # threading.Timer(0.2, ThreadedClient.periodicCall).start()


class SocketHandler:
    def __init__(self, conn):
        self.conn = conn

    def run(self):
        logger.info("SocketHandler started")
        cmd = ""
        try:
            logger.info("Calling blocking conn.recv()")
            cmd = str(self.conn.recv(1024))
            logger.info(cmd)
        except:
            logger.info("exception in conn.recv()") 
            # happens when connection is reset from the peer
        logger.info("Received cmd: " + cmd + " len: " + str(len(cmd)))
        #if len(cmd) == 0:
        #self.executeCommand(cmd)
        self.conn.close()
        #print "Client disconnected. Waiting for next client..."
        logger.info("SocketHandler terminated")

class ThreadedClient:
    """Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place."""
    rfid = RFIDReader()
    httpreq = HttpManager()
    loopinfo = GeneralInput()
    # barcode = USBBarcodeHandler()
    # qrcode = Barcode()
    messageflag = False
    enabledispenser = False
    ticket_at_front = False
    ticket_in = False
    timer = time.time()
    cpuTemp = CPUTemperature()
    looptimer = 0
    dispensertimer = 0
    barcodeResult = ""
    qrcodeResult = ""
    with open('/home/pi/AutoPark2020_Exit/TerminalSettings.json') as json_file:
            data = json.load(json_file)
    dispensername = data['dispenser-type']
    looptimerset = data["loop-time"]
    looptimerset = int(looptimerset)
    ticketdispenser_ = globals()['TicketDispenser' + dispensername]()
    dispensertimerset = 8
    periodicflag = False
    msg = 1

    def __init__(self, master):
        """Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O)."""
        self.master = master
        #self.machinestate = 0
        r = 1

        # Create the queue
        self.queue = queue.Queue()
        self.queuechk = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=getattr(self, 'workerThreadDispenser' + self.dispensername))
        self.thread1.start()
        self.thread2 = threading.Thread(target=self.workerThreadRFID)
        self.thread2.start()
        self.thread3 = threading.Thread(target=self.workerThreadQrCode)
        self.thread3.start()
        self.thread4 = threading.Thread(target=self.workerThreadListener)
        self.thread4.start()
        self.thread5 = threading.Thread(target=self.workerThreadUSBBarcode)
        self.thread5.start()
        self.thread6 = threading.Thread(target=self.workerThreadReadCPUTemp)
        self.thread6.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()
        #self.gui.processIncoming()


    def periodicCall(self):
        """Check every 200 ms if there is something new in the queue."""
        self.gui.processIncoming()
        #try:
        if self.queuechk.qsize():
            #self.gui.proccessIncoming()
            msgc = self.queuechk.get(0)
            logger.info("incoming msg: {}".format(msgc))
        #msgc = self.msg
            #time.sleep(0.1)
            if msgc == 1 or msgc == 506:
                #print("CHECK: {}".format(msgc))
                #self.gui.processIncoming()
                if not self.running:
                    # This is the brutal stop of the system. You may want to do
                    # some cleanup before actually shutting it down.
                    import sys
                    sys.exit(1)
                #self.MSGTimer(4)
                #self.MSGTimer(0.05)
                self.messageflag = True
                self.master.after(50, self.periodicCall)
                pass
            if msgc == 2:
                #print(self.queue.get(0))
                #print("CHECK: {}".format(self.msg))
                #self.gui.processIncoming()
                if not self.running:
                    # This is the brutal stop of the system. You may want to do
                    # some cleanup before actually shutting it down.
                    import sys
                    sys.exit(1)
                #self.master.after(50, self.periodicCall)
                self.messageflag = False
                self.master.after(50, self.periodicCall)
                pass
            if msgc == 201 or msgc == 200 or msgc == 505:
                logger.info("CHECK: {}".format(msgc))
                #self.gui.processIncoming()
                if not self.running:
                    # This is the brutal stop of the system. You may want to do
                    # some cleanup before actually shutting it down.
                    import sys
                    sys.exit(1)
                #self.MSGTimer(2)
                #self.master.after(50, self.periodicCall)
                self.messageflag = False
                self.master.after(2000, self.periodicCall)
                pass
            if msgc == 404 or msgc == 503 or msgc == 504 or msgc == 405 or msgc == 406 or msgc == 507:
                logger.info("CHECK: {}".format(msgc))
                #self.gui.processIncoming()
                if not self.running:
                    # This is the brutal stop of the system. You may want to do
                    # some cleanup before actually shutting it down.
                    import sys
                    sys.exit(1)
                #self.MSGTimer(4)
                #self.master.after(50, self.periodicCall)
                self.messageflag = False
                self.master.after(4000, self.periodicCall)
                #self.MSGTimer(4)
                pass
        else:
            while self.running == 1:
                if self.queuechk.qsize():
                    logger.info("passed")
                    self.master.after(10, self.periodicCall)
                    break
        #except:
            #self.master.after(200, self.periodicCall)
            #logger.info("Periodic Exception")
        
            
        """except:
            self.master.after(100, self.periodicCall)
            print("periodic exception")
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        # self.gui.processIncoming()"""

    def looptimer_tick(self):
        self.machinestate = 0
        
    def dispensertimer_tick(self):
        self.machinestate = 0
        
    def MSGTimer(self, msgtimeset):
        msgtimerstart = time.time()
        msgtimerset = 0
        while msgtimerset < msgtimeset:
            msgtimerset = time.time() - msgtimerstart
            msgtimerstart = time.time()

    def interrupted(self):
        "called when read times out"
        qrcodereading = raw_input()
        logger.info('...' + qrcodereading)
        return

    def workerThreadDispenserAdel(self):
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                self.ticketdispenser_.ticketdispenserstatuscmd()
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                logger.info(ticketdispenserrespcmd)
                #print(self.messageflag)
                if self.messageflag == False:
                    msg_screen = 1
                # if ticketdispenserrespcmd[3] == 5:
                #    pass
                # logger.info('no ticket @ front')
                # if ticketdispenserrespcmd[3] == 3 or ticketdispenserrespcmd[13] == 3 and len(str(ticketdispenserrespcmd)) >= 30:
                # elif ticketdispenserrespcmd[9] == 4:
                #    logger.info('TICKET DETECTED')
                #    self.ticketdispenser_.intaketochipcmd()
                try:
                    if ticketdispenserrespcmd[9] == 48:
                        self.enabledispenser = False
                        #self.messageflag = False
                        self.ticket_at_front = False
                        logger.info('no ticket @ front')
                    if ticketdispenserrespcmd[9] == 49 and self.enabledispenser == True and self.ticket_at_front == True:
                        logger.info('WAIT TO RETRIEVE TICKET')
                        #self.messageflag = True
                        msg_screen = 506
                    if ticketdispenserrespcmd[9] == 49 and self.enabledispenser == False:
                        # ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                        # print("Status: " + ticketdispenserbarc)
                        # time.sleep(0)
                        logger.info('TICKET DETECTED')
                        self.enabledispenser = True
                        self.ticketdispenser_.intaketochipcmd()
                        # ticketdispenser_.disableintaketochipcmd()
                        # ticketdispenser_.barcodereadingcmd()
                except:
                    logger.info("Problem with ticket or dispenser")
                    # self.ticketdispenser_.getinput()
                # self.machinestate = 1
                # looptimer = threading.Timer(10.0, self.looptimer_tick)
                # looptimer.start()
                    # self.queue.put(msg)
                time.sleep(0.2)
                logger.info('Barcode = ' + ticketdispenserbarc)
                if ticketdispenserbarc == '' or ticketdispenserrespcmd == b'\x06\x02035310001\x03':
                    msg_screen = 505
                    self.ticketdispenser_.returnticketcmd()
                elif 'x' not in ticketdispenserbarc:
                    logger.info("BARCODE = " + ticketdispenserbarc)
                    #print(int(ticketdispenserbarc))
                    # self.ticketdispenser_.getinput()
                    try:
                        resp, cont, head = self.httpreq.sendticketexit(ticketdispenserbarc)
                        #print("Hey: {}".format(resp))
                        c = json.loads(cont.decode('utf-8'))
                        msg_screen = resp
                        #print('resp= ' + int(resp))
                        if msg_screen == 503:
                            # self.ticketdispenser_.returnticketcmd()
                            # time.sleep(0.3)
                            # ticketdispenser_.resetticketcmd()
                            # time.sleep(2)
                            # self.enabledispenser = True
                            # ticketdispenser_.ticketdispenserstatuscmd()
                            # ticketdispenserrespcmd = ticketdispenser_.readticketdispenserresponse()
                            # print('...' + ticketdispenserrespcmd[9])
                            # while ticketdispenserrespcmd[9] == 49:
                            # self.msg = 506
                            # self.queue.put(msg)
                            # print('wait to retrieve ticket')
                            # else:
                            # self.enabledispenser = False
                            # return
                            ex = str(c['exception'])
                            logger.info(ex)
                        if msg_screen == 503 and ex == "TicketNotPaidException":
                            msg_screen = msg_screen + 1
                            logger.info(ex)
                            # print(type(msg))
                            #self.ticketdispenser_.returnticketcmd()
                            # time.sleep(0.3)
                            # ticketdispenser_.resetticketcmd()
                            # time.sleep(0.3)
                        if msg_screen == 503 and ex == "VehicleAlreadyExitedException":
                            msg_screen = 503
                            logger.info(ex)
                        if msg_screen == 503 and ex != "TicketNotPaidException" and ex != "VehicleAlreadyExitedException":
                            msg_screen = msg_screen +4
                            logger.info(ex)
                            #self.ticketdispenser_.returnticketcmd()
                        #if self.msg == 404:
                            #self.ticketdispenser_.returnticketcmd()
                        self.httpreq.receive_ticket_exit(resp)
                        self.ticket_at_front = True
                    except:
                        logger.info("BARCODE EXCEPTION")
                        pass
                    #self.httpreq.receive_ticket_exit(resp)
                timeout = 1
                logger.info('timer= ' + str(self.looptimer))
                self.looptimer =float(time.time() - self.timer)
                # self.enabledispenser = False
                '''i, o, e = select.select([sys.stdin], [], [], timeout)
                if i:
                    qrcodereading = sys.stdin.readline().strip()
                    logger.info("qrcode: " + qrcodereading)
                else:
                    logger.info('no qrcode')'''
            elif loopstate == 0 or self.looptimer > self.looptimerset:
                self.ticketdispenser_.ticketdispenserstatuscmd()
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                logger.info(ticketdispenserrespcmd)
                time.sleep(0.3)
                try:
                    if ticketdispenserrespcmd[10] == 49:
                        #self.ticketdispenser_.returnticketcmd()
                        self.ticketdispenser_.resetticketdispenser()
                except:
                    pass
                if self.enabledispenser == False:
                    self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    msg_screen = 2
                self.timer = time.time()
                #self.ticketdispenser_.resetticketdispenser()
            try:
                if self.msg != msg_screen:
                    self.msg = msg_screen
                    self.queue.put(msg_screen)
                    self.queuechk.put(msg_screen)
                    #print(self.queue.get(0))
					#print(msg_screen)
            except:
                logger.info('no msg on Adel Dispenser Thread')
           

    def workerThreadDispenserDDM(self):
        """This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly,
        by select or otherwise."""
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1  or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                logger.info(self.ticketdispenser_.ticketdispenserstatuscmd())
                ticketdispenserbarc, ticketdispenserrespcmd = self.ticketdispenser_.readticketdispenserresponse()
                logger.info(ticketdispenserrespcmd)
                if self.messageflag == False:
                    msg_screen = 1
                # if ticketdispenserrespcmd[3] == 5: pass logger.info('no ticket @ front') if ticketdispenserrespcmd[
                # 3] == 3 or ticketdispenserrespcmd[13] == 3 and len(str(ticketdispenserrespcmd)) >= 30: elif
                # ticketdispenserrespcmd[9] == 4: logger.info('TICKET DETECTED')
                # self.ticketdispenser_.intaketochipcmd()
                try:
                    if len(ticketdispenserrespcmd) <= 10:
                        logger.info('no ticket @ front')
                        pass
                    elif len(ticketdispenserrespcmd) > 10 and ticketdispenserrespcmd[3] == 3 or len(
                            ticketdispenserrespcmd) > 10 and ticketdispenserrespcmd[13] == 3:
                        # ticketdispenserbarc, ticketdispenserrespcmd =
                        # self.ticketdispenser_.readticketdispenserresponse()
                        logger.ingo("Status: " + ticketdispenserbarc)
                        # time.sleep(0)
                        logger.info('TICKET DETECTED')
                        self.ticketdispenser_.intaketochipcmd()
                except:
                    logger.info("Ticket Detection Problem")
                    # self.ticketdispenser_.getinput()
                # self.machinestate = 1
                # looptimer = threading.Timer(10.0, self.looptimer_tick)
                # looptimer.start()
                    # self.queue.put(msg)
                # time.sleep(0.5)
                if 'b' not in ticketdispenserbarc:
                    logger.info("BARCODE = " + ticketdispenserbarc)
                    logger.info(type(ticketdispenserbarc))
                    # self.ticketdispenser_.getinput()
                    if '<' in ticketdispenserbarc:
                        msg_screen = 505
                        self.ticketdispenser_.returnticketcmd()
                        #time.sleep(0.5)
                    try:
                        resp, cont, head = self.httpreq.sendticketexit(ticketdispenserbarc)
                        c = json.loads(cont.decode('utf-8'))
                        msg_screen = resp
                        if msg_screen == 503:
                            ex = str(c['exception'])
                            logger.info(ex)
                        if msg_screen == 503 and ex == "TicketNotPaidException":
                            msg_screen = msg_screen + 1
                            # print(type(msg))
                        elif msg_screen == 503 and ex != "TicketNotPaidException":
                            msg_screen = msg_screen + 4
                        self.httpreq.receive_ticket_exit(resp)
                    except:
                        logger.info("BARCODE EXCEPTION")
                        #print("ghgghjkmkhj")
                        #pass
                timeout = 1
                # self.enabledispenser = False
                '''i, o, e = select.select([sys.stdin], [], [], timeout)
                if i:
                    qrcodereading = sys.stdin.readline().strip()
                    logger.info("qrcode: " + qrcodereading)
                else:
                    logger.info('no qrcode')'''
                self.looptimer =float(time.time() - self.timer)
            elif loopstate == 0:
                if self.enabledispenser == False:
                    self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    msg_screen = 2
                self.timer = time.time()
                """try:
                    print(self.queue.get(0))
                except:
                    print("nothing at queue")"""
            try:
                if self.msg != msg_screen:
                    self.msg = msg_screen
                    self.queue.put(msg_screen)
                    self.queuechk.put(msg_screen)
                    #print(self.queue.get(0))
                #print(msg_screen)
            except:
                logger.info('no msg on DDM Thread')
                
    def workerThreadDispenserPico(self):
        """This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly,
        by select or otherwise."""
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1  or self.looptimer < self.looptimerset:
                print('loop was activated')
                self.ticketdispenser_.getTicketDispenserStatus()
                time.sleep(0.3)
                ticketdispenserrespcmd = self.ticketdispenser_.readTicketDispenserResponse()
                logger.info(ticketdispenserrespcmd)
                if ticketdispenserrespcmd == b'\x00\x01':
                    print('ticket @ front')
                    #if self.ticket_at_front == False:
                    self.ticketdispenser_.intaketochipcmd()
                    self.ticket_at_front = True
                    self.ticket_in = True
                    self.barcodeResult = ""
                elif ticketdispenserrespcmd == b'\x00\x00':
                    self.ticket_at_front = False
                    self.barcodeResult = ""
                    print('no ticket present')
                elif ticketdispenserrespcmd == b'\x00\x06' and self.barcodeResult == "":
                    self.ticketdispenser_.readPosition3TicketDispenserCmd()
                elif ticketdispenserrespcmd == b'\x00\x02' and self.barcodeResult == "":
                    for it in range(9):
                        self.ticketdispenser_.stepInTicketDispenserCmd()
                elif ticketdispenserrespcmd == b'\x00\x04' and self.barcodeResult == "":
                    self.ticketdispenser_.readPosition1TicketDispenserCmd()
                elif ticketdispenserrespcmd == b'\x00\x03' and self.barcodeResult == "" or ticketdispenserrespcmd == b'\x00\x03' and  not self.ticket_in:
                    self.ticketdispenser_.returnticketcmd()
                if self.messageflag == False:
                    msg_screen = 1
                self.looptimer = float(time.time() - self.timer)
            elif loopstate == 0:
                if self.enabledispenser == False:
                    self.enabledispenser = True
                if self.messageflag == True:
                    msg_screen = 2
                self.timer = time.time()
                """try:
                    print(self.queue.get(0))
                except:
                    print("nothing at queue")"""
            try:
                if self.msg != msg_screen:
                    self.msg = msg_screen
                    self.queue.put(msg_screen)
                    self.queuechk.put(msg_screen)
                    #print(self.queue.get(0))
                #print(msg_screen)
            except:
                logger.info('no msg on Pico Thread')
                

    def workerThreadUSBBarcode(self):
        '''DevicesList = open('/proc/bus/input/devices').readlines()
        if 'GD32icroelectronics GD32 Custm HID' in DevicesList[1]:
            device_event_number = DevicesList[5].split('event',1)[1]
            dev = '/dev/input/event' + device_event_number
        elif 'GD32icroelectronics GD32 Custm HID' in DevicesList[13]:
            device_event_number = DevicesList[17].split('event',1)[1]
            dev = '/dev/input/event' + device_event_number'''
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            DevicesList = open('/proc/bus/input/devices').readlines()
            if 'Newland Auto-ID DM21' in DevicesList[1]:
                device_event_number = DevicesList[5].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'Newland Auto-ID DM21' in DevicesList[13]:
                device_event_number = DevicesList[17].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'Newland Auto-ID DM21' in DevicesList[25]:
                device_event_number = DevicesList[29].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'Newland Auto-ID DM21' in DevicesList[37]:
                device_event_number = DevicesList[41].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            # dev = InputDevice('/dev/input/event1')
            # Provided as an example taken from my own keyboard attached to a Centos 6 box:
            scancodes = {
                # Scancode: ASCIICode
                0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
                10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
                20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
                30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
                40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
                50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
            }
            #result = ""
            for event in dev.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                   data = evdev.categorize(event)  # Save the event temporarily to introspect it
                   if data.keystate == 1:  # Down events only
                       key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                       print (key_lookup)  # Print it all out!
                       self.barcodeResult += key_lookup
                print('BARCODE DATA: ') # + str(self.barcodeResult))
                print(self.barcodeResult)
                if len(self.barcodeResult) >= 9:
                    self.barcodeResult = self.barcodeResult[:9]
                    try:
                        resp, cont, head = self.httpreq.sendticketexit(self.barcodeResult)
                        c = json.loads(cont.decode('utf-8'))
                        msg_screen = resp
                        if msg_screen == 503:
                            ex = str(c['exception'])
                            logger.info(ex)
                            # self.barcodeResult = ""
                            self.ticketdispenser_.returnticketcmd()
                            self.ticket_in = False
                        if msg_screen == 503 and ex == "TicketNotPaidException":
                            msg_screen = msg_screen + 1
                            # self.barcodeResult = ""
                            self.ticketdispenser_.returnticketcmd()
                            self.ticket_in = False
                        elif msg_screen == 503 and ex != "TicketNotPaidException":
                            msg_screen = msg_screen + 4
                            # self.barcodeResult = ""
                            self.ticketdispenser_.returnticketcmd()
                            self.ticket_in = False
                        elif msg_screen == 200 or msg_screen == 201:
                            self.ticketdispenser_.captureticketcmd()
                            # self.barcodeResult = ""
                            self.ticket_in = False
                        else:
                            self.ticketdispenser_.returnticketcmd()
                        self.httpreq.receive_ticket_exit(resp)
                        self.barcodeResult = ""
                        try:
                            if self.msg != msg_screen:
                                self.msg = msg_screen
                                self.queue.put(msg_screen)
                                self.queuechk.put(msg_screen)
                                #print(self.queue.get(0))
                                #print(msg_screen)
                        except:
                            logger.info('no msg on RFID Thread')
                    except:
                        logger.info("BARCODE HTTP EXCEPTION")
                elif len(self.barcodeResult) == 0 :
                    # self.ticket_in = False
                    self.barcodeResult = ""
                try:
                    if self.msg != msg_screen:
                        self.msg = msg_screen
                        self.queue.put(msg_screen)
                        self.queuechk.put(msg_screen)
                except:
                    logger.info("no msg on USB Barcode Thread")
                       

    def workerThreadRFID(self):
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                logger.info('loop was activated')
                self.machinestate = 1
                #looptimer = threading.Timer(10.0, self.looptimer_tick)
                #looptimer.start()
                #if self.messageflag == False:
                    #self.msg = 1
                    # self.queue.put(msg)
                time.sleep(0.5)
                msg = self.rfid.readrf()
                if len(str(msg)) > 4:
                    result = self.httpreq.sendcardexit(str(msg))
                    self.httpreq.receive_card_exit(result)
                    msg_screen = result
                    if msg_screen == 404:
                        msg_screen = msg_screen + 1
                    try:
                        if self.msg != msg_screen:
                            self.msg = msg_screen
                            self.queue.put(msg_screen)
                            self.queuechk.put(msg_screen)
                            #print(self.queue.get(0))
                        #print(msg_screen)
                    except:
                        logger.info('no msg on RFID Thread')
                    # self.queue.put(msg)
                # self.enabledispenser = False
            """elif loopstate == 0 and self.looptimer > self.looptimerset:
                if self.enabledispenser == False:
                    #self.ticketdispenser_.resetticketdispenser()
                    self.enabledispenser = True
                if self.messageflag == True:
                    msg_screen = 2"""
                #self.msg = msg_screen
                

    def workerThreadQrCode(self):
        self.queue.put(1)
        self.queuechk.put(1)
        while self.running:
            DevicesList = open('/proc/bus/input/devices').readlines()
            if 'USBKey Chip USBKey Module' in DevicesList[1]:
                device_event_number = DevicesList[5].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'USBKey Chip USBKey Module' in DevicesList[13]:
                device_event_number = DevicesList[17].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'USBKey Chip USBKey Module' in DevicesList[25]:
                device_event_number = DevicesList[29].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            elif 'USBKey Chip USBKey Module' in DevicesList[37]:
                device_event_number = DevicesList[41].split('event',1)[1]
                dev = InputDevice('/dev/input/event' + device_event_number.strip())
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            # dev = InputDevice('/dev/input/event0')
            # Provided as an example taken from my own keyboard attached to a Centos 6 box:
            scancodes = {
                # Scancode: ASCIICode
                0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
                10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
                20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
                30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
                40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
                50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
            }
            loopstate = self.loopinfo.readloopstate()
            barcode = '0'
            time.sleep(0.2)
            if loopstate == 1 or self.looptimer < self.looptimerset:
                print('loop was activated')
                self.machinestate = 1
                for event in dev.read_loop():
                    if event.type == evdev.ecodes.EV_KEY:
                       data = evdev.categorize(event)  # Save the event temporarily to introspect it
                       if data.keystate == 1:  # Down events only
                           key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                           print (key_lookup)  # Print it all out!
                           self.qrcodeResult += key_lookup
                    print('QRCODE DATA: ') # + str(self.qrcodeResult))
                    print(self.qrcodeResult)
                    if len(self.qrcodeResult) > 9:
                        self.qrcodeResult = self.qrcodeResult[:9]
                        try:
                            resp, cont, head = self.httpreq.sendticketexit(self.qrcodeResult)
                            c = json.loads(cont.decode('utf-8'))
                            msg_screen = resp
                            if msg_screen == 503:
                                ex = str(c['exception'])
                                logger.info(ex)
                                self.qrcodeResult = ""
                                # self.ticketdispenser_.returnticketcmd()
                                # self.ticket_in = False
                            if msg_screen == 503 and ex == "TicketNotPaidException":
                                msg_screen = msg_screen + 1
                                self.qrcodeResult = ""
                                # self.ticketdispenser_.returnticketcmd()
                                # self.ticket_in = False
                            elif msg_screen == 503 and ex != "TicketNotPaidException":
                                msg_screen = msg_screen + 4
                                self.qrcodeResult = ""
                                # self.ticketdispenser_.returnticketcmd()
                                # self.ticket_in = False
                            elif msg_screen == 201 or msg_screen == 200:
                                self.qrcodeResult = ""
                            elif msg_screen == 404:
                                self.qrcodeResult = ""
                            else:
                                # self.barcodeResult = ""
                                pass
                            self.httpreq.receive_ticket_exit(resp)
                            # time.sleep(0.5)
                            try:
                                if self.msg != msg_screen:
                                    self.msg = msg_screen
                                    self.queue.put(msg_screen)
                                    self.queuechk.put(msg_screen)
                                    #print(self.queue.get(0))
                                    #print(msg_screen)
                            except:
                                logger.info('no msg on RFID Thread')
                        except:
                            logger.info("QRCODE HTTP EXCEPTION")
                    elif len(self.qrcodeResult) == 0 :
                        self.qrcodeResult = ""
            elif loopstate == 0:
                self.qrcodeResult = ""
                if self.enabledispenser == False:
                    self.enabledispenser = True
                if self.messageflag == True:
                    msg_screen = 2
                self.timer = time.time()
            try:
                if self.msg != msg_screen:
                    self.msg = msg_screen
                    self.queue.put(msg_screen)
                    self.queuechk.put(msg_screen)
            except:
                logger.info("no msg on QRCode Thread")
                        
                    
    def workerThreadListener(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # close port when process exits:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        logger.info("Socket created")
        try:
            serverSocket.bind((HOSTNAME, IP_PORT))
        except socket.error as msg:
            #print "Bind failed:", msg[0], msg[1]
            sys.exit()
        serverSocket.listen(10)
        while self.running:
            # To simulate asynchronous I/O, we create a random number at random intervals.
            # Replace the following two lines with the real thing.
            relays = GeneralOutput()
            loopstate = self.loopinfo.readloopstate()
            time.sleep(0.2)
            self.machinestate = 1
            #if self.messageflag == False:
                #msg = 1
            #self.queue.put(msg)
            time.sleep(0.5)
            logger.info("Calling blocking accept()...")
    
            conn, addr = serverSocket.accept()
            data = str(conn.recv(1024))
            logger.info("received message:" + data)
            data = data.split("msg=",1)[1]
            logger.info(data)
            data = data.strip()
            logger.info(data)
            data = data.replace("@'","")
            logger.info(data)
            if(data == "0"):
                relays.setbarrierpin()
                relays.resetbarrierpin()
                msg_screen = 200
                try:
                    if self.msg != msg_screen:
                        self.msg = msg_screen
                        self.queue.put(msg_screen)
                        self.queuechk.put(msg_screen)
                        #print(self.queue.get(0))
                    #print(msg_screen)
                except:
                    logger.info('no msg')
                #self.queue.put(msg)
            #graphics_test.update()
            logger.info("Connected with client at " + addr[0])
            #socketHandler = SocketHandler(conn)
            # necessary to terminate it at program termination:
            #socketHandler.setDaemon(True)  
            #socketHandler.run()
            
        
    def workerThreadReadCPUTemp(self):
        while self.running:
            coolingFans = GeneralOutput()
            logger.info(self.cpuTemp.temperature)
            time.sleep(2)
            if self.cpuTemp.temperature > 50:
                coolingFans.setFanspin()
                logger.info('Cooling fans started')
            elif self.cpuTemp.temperature < 50:
                coolingFans.resetFanspin()
                logger.info('Cooling fans stopped')
    

    def endApplication(self):
        self.running = 0


root = Tk()
root.withdraw()

client = ThreadedClient(root)
root.mainloop()
