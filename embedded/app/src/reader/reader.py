import logging

import RPi.GPIO as GPIO

from .pn532 import *
from .i_reader import IReader

logger = logging.getLogger(__name__)


class Reader(IReader):

    def __init__(self):
        super().__init__()
        self.pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        # pn532 = PN532_I2C(debug=False, reset=20, req=16)
        # pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = self.pn532.get_firmware_version()
        logger.info(f'Found PN532 with firmware version: {ver}.{rev}')

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()

    def close(self):
        GPIO.cleanup()

    def read_once(self):
        # Check if a card is available to read
        uid = self.pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is None:
            return None

        output = int.from_bytes(uid, byteorder='big')
        logger.info(f'Found card with UID: {output}')
        return output

    def read_loop(self):
        try:
            logger.info('Waiting for RFID/NFC card...')
            while True:
                self.read_once()

        except Exception as e:
            logger.exception("RFID Loop Exception")
        finally:
            self.close()
