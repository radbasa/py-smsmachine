#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import logging
import time
from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException, CommandError

# file = sys.argv[1]
# device = sys.argv[2]
# 

unit = str(sys.argv[1])
device = str(sys.argv[2])
cardcode = str(sys.argv[3]) + "#"
cardpin = str(sys.argv[4]) + "#"

BAUDRATE = 115200
LOADCODE = '223'

logging.basicConfig(filename="logs/" + unit + ".log", level = logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s');

# logging.info("Use file %s", file)
# logging.info("Use dev %s", device)

logging.info("Initializing modem...")

modem = GsmModem(device, BAUDRATE)
modem.connect()

logging.info("Waiting for network coverage...")
modem.waitForNetworkCoverage(30)

logging.info("Loading %s with %s %s", unit, cardcode, cardpin)
call = modem.dial( LOADCODE)

wasAnswered = False

while call.active:
    if call.answered:
        wasAnswered = True
        logging.info("Call answered")
        time.sleep(5.0)
        logging.info("DTMF card number")
        
        try:
            if call.active:
                call.sendDtmfTone( cardcode )
        except InterruptedException as e:
            logging.info("Card number DTMF playback interrupted: {0} ({1} Error {2})".format(e, e.cause.type, e.cause.code))
        except CommandError as e:
            logging.info('Card number DTMF playback failed: {0}'.format(e))


        time.sleep(5.0)
        
        try:
            if call.active:
                call.sendDtmfTone(cardpin)
        except InterruptedException as e:
            logging.info("Card pin DTMF playback interrupted: {0} ({1} Error {2})".format(e, e.cause.type, e.cause.code))
        except CommandError as e:
            logging.info('Card pin DTMF playback failed: {0}'.format(e))

        time.sleep(10.0)
        
        if call.active:
            logging.info("Hanging up call")
            call.hangup()
        else:
            logging.info("Call ended by remote party")
    else:
        logging.info("Wait")
        time.sleep(2.0)

if not wasAnswered:
    logging.info("Call was not answered")

logging.info("Load process done.")
modem.close()
