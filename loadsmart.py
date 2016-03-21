#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import logging
import time
from gsmmodem.modem import GsmModem

# file = sys.argv[1]
# device = sys.argv[2]
# 

unit = str(sys.argv[1])
device = str(sys.argv[2])
cardcode = str(sys.argv[3])

BAUDRATE = 115200
LOADCODE = '1510'

logging.basicConfig(filename="logs/" + unit + ".log", level = logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s');

# logging.info("Use file %s", file)
# logging.info("Use dev %s", device)

logging.info("Initializing modem...")

modem = GsmModem(device, BAUDRATE)
modem.smsTextMode = False
modem.connect()

logging.info("Waiting for network coverage...")
modem.waitForNetworkCoverage(30)

logging.info("Loading %s with %s", unit, cardcode)
call = modem.dial( LOADCODE + cardcode)

wasAnswered = False

while call.active:
    if call.answered:
        wasAnswered = True
        logging.info("Call answered")
        time.sleep(10.0)
        if call.active:
            logging.info("Hanging up")
            call.hangup()
        else:
            logging.info("Call ended by remote party")
    else:
        time.sleep(0.5)

if not wasAnswered:
    logging.info("Call was not answered")

logging.info("Load process done.")
modem.close()
