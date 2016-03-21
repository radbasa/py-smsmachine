#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import time
from gsmmodem.modem import GsmModem
from gsmmodem import pdu

# file = sys.argv[1]
# device = sys.argv[2]
# 

unit = sys.argv[1]
device = sys.argv[2]

BAUDRATE = 115200
BALCODE = "?1515"
BALDIAL = "214"

logging.basicConfig(filename="logs/" + unit + ".log", level = logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s');

# logging.info("Use file %s", file)
# logging.info("Use dev %s", device)

logging.info("Initializing modem...")

modem = GsmModem(device, BAUDRATE)
modem.smsTextMode = True
modem.connect()

logging.info("Waiting for network coverage...")
modem.waitForNetworkCoverage(30)

logging.info("Check balance %s", unit)

modem.sendSms(BALDIAL, BALCODE)

logging.info("Balance request done")
modem.close()