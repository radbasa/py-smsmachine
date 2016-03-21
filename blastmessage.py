#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
import logging
import time
from gsmmodem.modem import GsmModem
from gsmmodem import pdu
from gsmmodem.exceptions import InterruptedException, CommandError, TimeoutException

# file = sys.argv[1]
# device = sys.argv[2]
# 
def handleSms(sms):
    logging.info("REPLY %s: %s", sms.number, sms.text)
    modem.deleteMultipleStoredSms(delFlag=1)

unit = sys.argv[1]
device = sys.argv[2]
message = "Message"

BAUDRATE = 115200

logging.basicConfig(filename="logs/" + unit + ".log", level = logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s');

# logging.info("Use file %s", file)
# logging.info("Use dev %s", device)

logging.info("Initializing modem...")

modem = GsmModem(device, BAUDRATE, smsReceivedCallbackFunc=handleSms)
modem.smsTextMode = True
modem.connect()

logging.info("Waiting for network coverage...")
modem.waitForNetworkCoverage(30)

with open( 'data/' + unit + '.csv', 'rU' ) as csvfile:
    thisList = csv.reader(csvfile, delimiter=',', quotechar='"')
    head = next(thisList)
    
    totalrows = 0
    for row in thisList:
        totalrows += 1
        phone = '0' + str(row[0])
        logging.info("%s Send to %s", totalrows, phone)
        try:
            modem.sendSms(phone,message, deliveryTimeout=30)
        except CommandError as e:
            logging.info('SMS send failed: {0}'.format(e))
        except TimeoutException as e:
            logging.info('SMS timeout failed: {0}'.format(e))
        time.sleep(10.0)

logging.info("Blasting done")
modem.close()
