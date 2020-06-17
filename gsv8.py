# -*- coding: utf-8 -*-
"""
Datum 01.2016
@author: ME-Meßsysteme GmbH, Robert Bremsat, Dennis Rump
@version 1.2
"""
from ThreadSafeVar import TSVar

__author__ = 'Robert bremsat & Dennis Rump'
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015 ME-Meßsysteme GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Hiermit wird unentgeltlich, jeder Person, die eine Kopie der Software
# und der zugehörigen Dokumentationen (die "Software") erhält, die
# Erlaubnis erteilt, uneingeschränkt zu benutzen, inklusive und ohne
# Ausnahme, dem Recht, sie zu verwenden, kopieren, ändern, fusionieren,
# verlegen, verbreiten, unter-lizenzieren und/oder zu verkaufen, und
# Personen, die diese Software erhalten, diese Rechte zu geben, unter
# den folgenden Bedingungen:
#
# Der obige Urheberrechtsvermerk und dieser Erlaubnisvermerk sind in
# alle Kopien oder Teilkopien der Software beizulegen.
#
# DIE SOFTWARE WIRD OHNE JEDE AUSDRÜCKLICHE ODER IMPLIZIERTE GARANTIE
# BEREITGESTELLT, EINSCHLIESSLICH DER GARANTIE ZUR BENUTZUNG FÜR DEN
# VORGESEHENEN ODER EINEM BESTIMMTEN ZWECK SOWIE JEGLICHER
# RECHTSVERLETZUNG, JEDOCH NICHT DARAUF BESCHRÄNKT. IN KEINEM FALL SIND
# DIE AUTOREN ODER COPYRIGHTINHABER FÜR JEGLICHEN SCHADEN ODER SONSTIGE
# ANSPRUCH HAFTBAR ZU MACHEN, OB INFOLGE DER ERFÜLLUNG VON EINEM
# VERTRAG, EINEM DELIKT ODER ANDERS IM ZUSAMMENHANG MIT DER BENUTZUNG
# ODER SONSTIGE VERWENDUNG DER SOFTWARE ENTSTANDEN.
#
###############################################################################

import copy
import logging
import threading
from queue import Queue
from collections import deque
import time
import serial
from GSV6_FrameRouter import FrameRouter
from GSV6_Protocol import GSV_6Protocol
from GSV6_SeriallLib import GSV6_seriall_lib
from GSV_BasicMeasurement import BasicMeasurement

'''
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
import sys
from twisted.internet.error import ReactorAlreadyInstalledError
'''

# load default Logging config
from GSV_Exceptions import GSV6_ConversionError_Exception, GSV_CommunicationException

logging.basicConfig()

useTwisted = False


class ThreadingReadFromSerial(threading.Thread):
    def __init__(self, gsvSerialPort, serialProtocol):
        threading.Thread.__init__(self)
        self.gsvSerialPort = gsvSerialPort
        self.serialProtocol = serialProtocol
        self.runnng = True
        self.setDaemon(True)

    def run(self):
        while (self.runnng):
            if (serial.VERSION[0] == '2'):
                bytesToRead = self.gsvSerialPort.inWaiting()
            else:
                bytesToRead = self.gsvSerialPort.in_waiting
            if (bytesToRead > 0):
                self.serialProtocol.dataReceived(bytearray(self.gsvSerialPort.read(bytesToRead)))
            #time.sleep(0.001)

    def stop(self):
        self.runnng = False


class gsv8:
    """

    Die Klasse gsv8 stellt alle GSV-8 Methoden zur Verfügung. Sie müssen in Ihrem Python Script ein Objekt für jeden
    GSV-8 erstellen, um ein Objekt zu erzeugen verwenden Sie Variable = gsv8(port, baudrate)
    Sie können mehrere GSV8-Objekte erzeugen.

    :param port: Name des zu verwenden seriellen ports
    :param baudrate: Bautrate
    """

    _gsvSerialPort = None

    # The Queue-Object is an threadsafe FIFO Buffer.
    # Operations like put and get are atomic
    # this queue holds all incomming complete Frames
    _frameInBuffer = Queue(50)

    # this queue holds the ordered config requests
    _antwortQueue = Queue(50)

    # _messwertRotatingQueue = deque([], 1)
    _lastMesswert = TSVar()

    # GSV Lib
    _gsvLib = None

    transmissionIsRunning = True

    def __init__(self, port, baudrate):
        logging.getLogger('gsv8').setLevel(logging.INFO)
        logging.getLogger('gsv8').info('Start with config: Serialport: {}; Baudrate: {};'.format(port, baudrate))

        '''
        if (useTwisted):
            if sys.platform == 'win32':
                # on windows, we need to use the following reactor for serial support
                # http://twistedmatrix.com/trac/ticket/3802
                ##
                from twisted.internet import win32eventreactor

                try:
                    win32eventreactor.install()
                except ReactorAlreadyInstalledError:
                    pass
        '''
        if (not useTwisted):
            self._gsvSerialPort = serial.Serial()

            self._gsvSerialPort.baudrate = baudrate
            self._gsvSerialPort.port = port
            self._gsvSerialPort.parity = serial.PARITY_NONE
            self._gsvSerialPort.stopbits = serial.STOPBITS_ONE
            self._gsvSerialPort.bytesize = 8
            self._gsvSerialPort.timeout = 1
            self._gsvSerialPort.open()

        self._gsvLib = GSV6_seriall_lib();
        # create GSV6 Serial-Protocol-Object
        self.serialProtocol = GSV_6Protocol(self._frameInBuffer, self._antwortQueue)

        if (useTwisted):
            '''
            try:
                self._gsvSerialPort = SerialPort(self.serialProtocol, port, reactor, baudrate=baudrate)
            except Exception as e:
                logging.getLogger('gsv8t').critical('Could not open serial port: {0}. exit!'.format(e))
                raise Exception()
            '''
        else:
            self.serialReadThread = ThreadingReadFromSerial(self._gsvSerialPort, self.serialProtocol)

        # create an router object/thread
        # self.router = FrameRouter(self._frameInBuffer, self._antwortQueue, self._messwertRotatingQueue, self._gsvLib)
        self.router = FrameRouter(self._frameInBuffer, self._antwortQueue, self._lastMesswert, self._gsvLib)

        # start threaded read from serial
        if (not useTwisted):
            self.serialReadThread.start()

        # start frame-router-thread
        self.router.start()

        result = self.StopTransmission()
        if (result[0] == 0x00):
            logging.getLogger('gsv8').info('GSV8 detected and stopped.')
        else:
            logging.getLogger('gsv8').critical('some error occurred; GSV answer: ' + str(result))

    def __del__(self):
        if (not useTwisted):
            self.serialReadThread.stop()
        self.router.stop()
        self.router.stopCSVRecording()

    def isResultOk(self, result):
        '''
        Die Methode erhält die Ergebnisliste (AntwortErrorCode und AntwortErrorText) und gibt True zurück, wenn kein Fehler vorliegt.

        :return: True wenn AntwortErrorCode == 0x00; False wenn AntwortErrorCode != 0x00
        :rtype: bool
        '''
        if (result[0] == 0):
            return True
        else:
            return False

    def StopTransmission(self):
        '''
        Die Methode StopTransmission teilt dem GSV mit, das die Messwertübertragung angehalten werden soll.
        Sobald der Befehl abgesendet wird sendet der GSV8 keine Messdaten mehr über die serielle Schnittstelle.
        Sie können StartTransmission verwenden um die Übertragung erneut zu starten.
        Verwenden Sie getValue um einzel Werte abzurufen.

        :return: AntwortCode und AntwortErrorText
        :rtype: liste
        '''

        if not self.transmissionIsRunning:
            return

        # erstelle zu sendene Bytefolge für StopTransmission
        output = self._gsvLib.buildStopTransmission()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            self.transmissionIsRunning = False
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def StartTransmission(self):
        '''
        Die Methode StartTransmission teilt dem GSV mit, das er Messdaten senden darf.

        :return: AntwortCode und AntwortErrorText
        :rtype: liste
        '''
        if self.transmissionIsRunning:
            return

        # erstelle zu sendene Bytefolge für StartTransmission
        output = self._gsvLib.buildStartTransmission()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            self.transmissionIsRunning = True
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def setTXmodefloat(self):
        '''
        Setzt float als Messwert-Datenformat

        :return: AntwortCode und AntwortErrorText
        :rtype: the return type description
        '''

        # command = array.array('B', [0xAA, 0x93, 0x81, 0x03, 0x00, 0x10, 0x85]).tostring()
        # self.gsvSerialPort.write(command)

        # erstelle zu sendene Bytefolge für setTXmodefloat
        output = self._gsvLib.buildSetTXModeToFloat()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

    def ReadValue(self):
        '''
        Die Methode ruft einmal Messwerte vom GSV ab (one shot).

        :return: AntwortCode und AntwortErrorText
        :rtype: liste
        '''

        if(self.transmissionIsRunning):
            # return self._messwertRotatingQueue[0]
            result = copy.deepcopy(self._lastMesswert.getVar())
        else:
            # alte Messwerte löschen
            # self._messwertRotatingQueue.clear()
            self._lastMesswert.setVar(None)

            # erstelle zu sendene Bytefolge für GetValue (OneShot)
            output = self._gsvLib.buildGetValue()

            # sende Daten via serialport
            self._gsvSerialPort.write(output)

            # ersten AntwortFrame aus der Queue holen
            # hier keine Antwort!!!

            # [seconds]
            abort_after = 2
            start = time.time()

            result = None
            # auf Messwert warten, aber maximal 2 sec.
            while True:
                try:
                    #result = copy.deepcopy(self._messwertRotatingQueue.pop())
                    # result = copy.copy(self._messwertRotatingQueue[0])
                    tmp = self._lastMesswert.getVar()
                    if(tmp != None):
                        result = copy.copy(tmp)
                        break
                except IndexError:
                    pass

                # timeout berechnung
                delta = time.time() - start
                if delta >= abort_after:
                    break

            # return BasicMeasurement(result)
        return BasicMeasurement(result)

    def SetZero(self, channel):
        '''
        Die Methode setzt die Kanäle des GSV null.

        :return: AntwortCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für SetZero
        output = self._gsvLib.buildWriteSetZero(channel)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

    def getDIOdirection(self, gruppe):
        '''
        Ruft die DIOdirection vom GSV ab

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :type gruppe: uint8
        :return: AntwortCode und AntwortErrorText
        :rtype: liste
        '''
        # erstelle zu sendene Bytefolge für getDIOdirection
        output = self._gsvLib.buildGetDIOdirection(gruppe)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = antwortFrame.getPayload()[0]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def isDIOgroupOutput(self, gruppe):
        '''
        gibt True zurueck, wenn die Direction der gewaehlten DIO Gruppe als  Output konfiguriert ist.

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :type gruppe: uint8
        :return: True wenn die Direction der DIO Gruppe Output ist, False wenn die Direction der DIO Gruppe kein Output ist (als Input)
        :rtype: bool
        '''

        if (self.getDIOdirection(gruppe) == 0x00):
            return True
        else:
            return False

    def isDIOgroupInput(self, gruppe):
        '''
        gibt True zurueck, wenn die Direction der gewaehlten DIO Gruppe als  Input konfiguriert ist.

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :type gruppe: uint8
        :return: True wenn die Direction der DIO Gruppe Input ist, False wenn die Direction der DIO Gruppe kein Input ist (als Output)
        :rtype: bool
        '''
        return not self.isDIOgroupOutput(gruppe)

    def setDIOdirection(self, gruppe, direction):
        '''
        setzt die DIOdirection der jeweiligen Gruppe vom GSV

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :param direction: Muss die DIO Gruppendirection beinhalten
        :type gruppe: uint8
        :type direction: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildSetDIOdirection(gruppe, direction)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

    def setDIOgroupToOutput(self, gruppe):
        '''
        Setzt die Direction der Gruppe zu Output

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :type gruppe: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.setDIOdirection(gruppe, 0)

    def setDIOgroupToInput(self, gruppe):
        '''
        Setzt die Direction der Gruppe zu Input

        :param gruppe: Muss die DIO Gruppennummer beinhalten
        :type gruppe: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.setDIOdirection(gruppe, 1)

    def getDIOlevel(self, IOPin):
        '''
        Ruft das jeweilige DIOlevel vom GSV ab

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: 0 wenn Low; 1 wenn high
        :rtype: uint8
        '''
        # erstelle zu sendene Bytefolge für getDIOlevel
        output = self._gsvLib.buildGetDIOlevel(IOPin)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = self._gsvLib.convertToUint16_t(antwortFrame.getPayload())[0]

        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def setDIOlevel(self, IOPin, level):
        '''
        Setzt das DIO level am gewünschten Pin
        level 1 = high 0 low

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param level: high=1; low=0
        :type IOPin: uint8
        :type level: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildSetDIOlevel(IOPin, level)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def setPinToHigh(self, IOPin):
        '''
        Setzt IOPin auf High

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.setDIOlevel(IOPin, 1)

    def setPinToLow(self, IOPin):
        '''
        Setzt IOPin auf Low

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.setDIOlevel(IOPin, 0)

    def isPinHigh(self, IOPin):
        '''
        IOPin level Abfrage

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: True wenn IOPin High; False wenn IOPin Low
        :rtype: bool
        '''
        if (IOPin == 0):
            raise Exception('Dieser Befehl ist nicht auf alle Kanaele gleichzeitig anwendbar.')

        if (self.getDIOlevel(IOPin) == 0):
            return False
        else:
            return True

    def isPinLow(self, IOPin):
        '''
        IOPin level Abfrage

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: True wenn IOPin Low; False wenn IOPin High
        :rtype: bool
        '''
        return not self.isPinHigh(IOPin)

    def getDIOinitialLevel(self, IOPin):
        '''
        Ruft das jeweilige initial DIOlevel vom GSV ab

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: 0 wenn Low; 1 wenn high
        :rtype: uint8
        '''
        # erstelle zu sendene Bytefolge für getDIOlevel
        output = self._gsvLib.buildGetDIOinitialLevel(IOPin)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = self._gsvLib.convertToUint16_t(antwortFrame.getPayload())[0]

        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def setDIOinitialLevel(self, IOPin, level):
        '''
        Setzt das DIO level am gewünschten Pin
        level 1 = high 0 low

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param level: high=1; low=0
        :type IOPin: uint8
        :type level: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildSetDIOinitialLevel(IOPin, level)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def writeDataRate(self, frequenz):
        '''
        Setzt die Datenrate in Hz

        :param frequenz: Gibt die gewuenschte Frequenz in Hz an
        :type frequenz: float
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # frequenz umwandeln
        data = self._gsvLib.convertFloatToBytes(frequenz)
        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildWriteDataRate(data)
        # sende Daten via serialport
        self._gsvSerialPort.write(output)
        
        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

    def readDataRate(self):
        '''
        Ließt die Datenrate in Hz

        :return: Frequenz in Hz
        :rtype: float
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildGetDataRate()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0):
            result = self._gsvLib.convertToFloat(antwortFrame.getPayload())[0]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def isSixAxisMatrixActive(self):
        '''
        gibt den Status der Calibration Matrix wieder

        :return: True wenn Matrix aktiv; False wenn Matrix inaktiv
        :rtype: bool
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildGetMode()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() != 0):
            # return [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText(), 'Get']
            return False

        # Fehlerall
        if (len(antwortFrame.getPayload()) != 4):
            return None

        flags = antwortFrame.getPayload()

        if ((flags[3] & 0x01) == 1):
            return True
        else:
            return False

    def setSixAxisMatrixActive(self, state):
        '''
        Setzt den Status der Calibration Matrix (aktiv oder inaktiv)

        :param state: gewuenschter neuer Status der Matrix
        :type state: bool
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildGetMode()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() != 0):
            return [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText(), 'Get']

        # Fehlerall
        if (len(antwortFrame.getPayload()) != 4):
            return None

        flags = antwortFrame.getPayload()

        if (state):
            # set to active
            flags[3] = flags[3] | 0x01
        else:
            # set to inactive
            flags[3] = flags[3] & 0xFE

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildSetMode(flags)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)
        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        result = None
        if (antwortFrame.getAntwortErrorCode() == 0):
            [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def writeDIOthreshold(self, IOPin, upper_or_lower_trigger, threshold_value):
        '''
        Setzt die oberen oder unteren Schwellwert für den angegeben IO Pin

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param upper_or_lower_trigger: Lower=0; Upper=1
        :param threshold_value: Schwellwert
        :type IOPin: uint8
        :type upper_or_lower_trigger: uint8
        :type threshold_value: float
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für writeDIOthreshold
        output = self._gsvLib.buildWriteDIOthreshold(IOPin, upper_or_lower_trigger, threshold_value)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def writeLowerDIOthreshold(self, IOPin, threshold_value):
        '''
        Setzt den unteren Schwellwert des gegeben IOPin´s

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param threshold_value: Schwellwert
        :type IOPin: uint8
        :type threshold_value: float
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.writeDIOthreshold(IOPin, 0, threshold_value)

    def writeUpperDIOthreshold(self, IOPin, threshold_value):
        '''
        Setzt den oberen Schwellwert des gegeben IOPin´s

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param threshold_value: Schwellwert
        :type IOPin: uint8
        :type threshold_value: float
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        return self.writeDIOthreshold(IOPin, 1, threshold_value)

    def readDIOthreshold(self, IOPin, upper_or_lower_trigger):
        '''
        Ließt die oberen oder unteren Schwellwert für den angegeben IOPin

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param upper_or_lower_trigger: Lower=0; Upper=1
        :type IOPin: uint8
        :type upper_or_lower_trigger: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für readDIOthreshold
        output = self._gsvLib.buildReadDIOthreshold(IOPin, upper_or_lower_trigger)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0):
            result = self._gsvLib.convertToFloat(antwortFrame.getPayload())[0]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def readLowerDIOthreshold(self, IOPin):
        '''
        Ließt den unteren Schwellwert des angegeben IOPin´s

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: unterer Schwellwert
        :rtype: float
        '''
        return self.readDIOthreshold(IOPin, 0)

    def readUpperDIOthreshold(self, IOPin):
        '''
        Ließt den oberen Schwellwert des angegeben IOPin´s

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: unterer Schwellwert
        :rtype: float
        '''
        return self.readDIOthreshold(IOPin, 1)

    def setUserScaleBySensor(self, kanal, sensor_messbereich, sensor_kennwert):
        '''
        Errechnet und setzt einen neuen ScalierungsFaktor fuer den jeweiligen DMS-Kanal

        :param kanal: DMS-Kanal 1..8 oder 0
        :param sensor_messbereich: Messbereich des Sensors
        :param sensor_kennwert: IOPin Kennwert des Sensors
        :type kanal: uint8
        :type sensor_messbereich: float
        :type sensor_kennwert: float
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für readDIOthreshold
        output = self._gsvLib.buildReadInputType(kanal, 0xFF)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0):
            sensIndex = antwortFrame.getPayload()[0]
            sense = self._gsvLib.convertToUint32_t(antwortFrame.getPayload()[1:])[0]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        newUserScale = (sensor_messbereich / sensor_kennwert) * (sense / 100)

        # frequenz umwandeln
        data = self._gsvLib.convertFloatToBytes(newUserScale)
        # erstelle zu sendene Bytefolge für WriteUserScale
        output = self._gsvLib.buildWriteUserScale(kanal, data)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def setDIOtype(self, IOPin, dioType, assignedDMSchannel=0):
        '''
        Setzt DIOtype für den angegeben IO Pin

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param dioType: DIO Type aus Datenblatt
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type dioType: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für SetDIOtype
        output = self._gsvLib.buildSetDIOtype(IOPin, dioType, assignedDMSchannel)
        # print 'output: ' + ' '.join(format(x, '02x') for x in bytearray(output))


        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen

        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

    def setOutputHighByThreshold(self, IOPin, assignedDMSchannel):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wird auf high wenn Messwert unterhalb des unteren Schwellwerts faellt und low wenn er ueber den oberen Schwellwert steigt

        :parameter: IOPin: 1..16; assignedDMSchannel uint8

        :rtype: [antwortFrame.ErrorCode, AntwortErrorText]

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x01, 0x00, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, assignedDMSchannel)

    def setOutputLowByThreshold(self, IOPin, assignedDMSchannel):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wir auf low wenn Messwert unterhalb des unteren Schwellwerts faellt und high wenn er ueber den oberen Schwellwert steigt

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x81, 0x00, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, assignedDMSchannel)

    def setOutputHighIfOutsideWindow(self, IOPin, assignedDMSchannel):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wir auf low geschaltet solange der aktuelle Messwert sich innerhlab der gesetzten Schwellwerte befindet

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x81, 0x20, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, assignedDMSchannel)

    def setOutputHighIfInsideWindow(self, IOPin, assignedDMSchannel):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wir auf low geschaltet solange der aktuelle Messwert sich außerhalb der gesetzten Schwellwerte befindet

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x01, 0x20, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, assignedDMSchannel)

    def setInputToTaraInputForAllChannels(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin muss im Vorfeld als Eingang (Input) konfiguriert werden. Wird dieser Eingang high, wird Tara für alle DMS-Eingaenge aufgerufen

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11

        newDIOtype = bytearray([0x00, 0x00, 0x20])
        return self.setDIOtype(IOPin, newDIOtype, 0)

    def setInputToTaraInputForChannel(self, IOPin, assignedDMSchannel):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin muss im Vorfeld als Eingang (Input) konfiguriert werden. Wird dieser Eingang high, wird für den gewaehlte DMS-Eingang Tara aufgerufen

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x00, 0x10])
        return self.setDIOtype(IOPin, newDIOtype, assignedDMSchannel)

    def setStartTransmissionByInputIsHigh(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin muss im Vorfeld als Eingang (Input) konfiguriert werden. Wird dieser Eingang high, versendet der GSV8 mit der konfigurierten Datenrate Messwert-Frames

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x08, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, 0)

    def setDIOtoGenralPurposeInput(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Fuer den gewaehlte IOPin wird der DIOtype Genral-Purpose Input gesetzt

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type dioType: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x00, 0x04])
        return self.setDIOtype(IOPin, newDIOtype)

    def setDIOtoGenralPurposeOutput(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Fuer den gewaehlte IOPin wird der DIOtype Genral-Purpose Out gesetzt

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :param assignedDMSchannel: zugehoeriger DMS-Kanal; default=0
        :type IOPin: uint8
        :type assignedDMSchannel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x10, 0x00])
        return self.setDIOtype(IOPin, newDIOtype)

    def setPinTypeToInput(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wird als Input konfiguriert, hierbei ist die Gruppenrichtung (Input oder output) zu beachten

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x00, 0x04])
        return self.setDIOtype(IOPin, newDIOtype, 0)

    def setPinTypeToOutput(self, IOPin):
        '''
        Setzt DIOtype für den angegeben IO Pin
        Der gewaehlte IOPin wird als Output konfiguriert, hierbei ist die Gruppenrichtung (Input oder output) zu beachten

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Tabelle Typen der digitalen Ein- und Ausgaenge des GSV-8 pos. 11
        newDIOtype = bytearray([0x00, 0x10, 0x00])
        return self.setDIOtype(IOPin, newDIOtype, 0)

    def getDIOtype(self, IOPin):
        '''
        Ließt den gesetzten DIOtype für den angegeben IO Pin aus

        :param IOPin: IOPin 1..16 (1.1 - 4.4)
        :type IOPin: uint8
        :return: assignedDMSchannel und DIOtype
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für readDIOthreshold
        output = self._gsvLib.buildGetDIOtype(IOPin)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if (antwortFrame.getAntwortErrorCode() == 0):
            dioType = self._gsvLib.convertToUint24_t(antwortFrame.getPayload()[0:3])[0]
            assignedDMSchannel = antwortFrame.getPayload()[3]
            result = {}
            result['DIOtype'] = dioType
            result['assignedDMSchannel'] = assignedDMSchannel
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def startCSVrecordingWithoutStartTransmisson(self, csvFilepath, prefix=''):
        '''
        Start der Messwertaufnahme. Anfallende Messwerte werden in einer CSV-Datei gespeichert.
        Der Dateiname orientiert sich an dem aktuelen Datum und der aktuellen Uhrzeit

        *Achtung* Es wird KEIN StartTransmission aufgerufen!

        *Achtung* CSV-Dateipfad muss vorhanden sein!

        :param csvFilepath: Zielpfad fuer die CSV-Datei
        :type csvFilepath: String
        '''
        self.router.startCSVRecording(csvFilepath, prefix)

    def startCSVrecording(self, csvFilepath, prefix=''):
        '''
        Start der Messwertaufnahme. Anfallende Messwerte werden in einer CSV-Datei gespeichert.
        Der Dateiname orientiert sich an dem aktuelen Datum und der aktuellen Uhrzeit

        *Achtung* Es wird StartTransmission aufgerufen!

        *Achtung* CSV-Dateipfad muss vorhanden sein!

        :param csvFilepath: Zielpfad fuer die CSV-Datei
        :type csvFilepath: String
        '''
        if not self.router.isRecording():
            self.router.startCSVRecording(csvFilepath, prefix)
            self.StartTransmission()

    def startCSVrecording(self, frequenz, csvFilepath, prefix=''):
        '''
        Start der Messwertaufnahme. Anfallende Messwerte werden in einer CSV-Datei gespeichert.
        Der Dateiname orientiert sich an dem aktuelen Datum und der aktuellen Uhrzeit

        *Achtung* Es wird StartTransmission aufgerufen!

        *Achtung* CSV-Dateipfad muss vorhanden sein!

        :param frequenz: Gibt die gewuenschte Frequenz in Hz an
        :param csvFilepath: Zielpfad fuer die CSV-Datei
        :type frequenz: float
        :type csvFilepath: String
        '''
        if not self.router.isRecording():
            self.writeDataRate(frequenz)
            self.router.startCSVRecording(csvFilepath, prefix)
            self.StartTransmission()

    def stopCSVrecordingWithoutStopTransmission(self):
        '''
        Stoppt die Messwertaufnahme.

        *Achtung* Es wird KEIN StopTransmission aufgerufen!
        '''

        self.router.stopCSVRecording()

    def stopCSVrecording(self):
        '''
        Stoppt die Messwertaufnahme.

        *Achtung* Es wird StopTransmission aufgerufen!
        '''
        if self.router.isRecording():
            self.router.stopCSVRecording()
            self.StopTransmission()

    def get1wireTempValue(self):
        '''
        Die Methode get1wireTempValue holt 1wire temp value

        :return: Tempvalue
        :rtype: float
        '''

        # erstelle zu sendene Bytefolge für WriteDataRate
        output = self._gsvLib.buildGet1WireTempValue()

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen
        if ((antwortFrame.getAntwortErrorCode() == 0) and (len(antwortFrame.getPayload()) == 4)):
            return self._gsvLib.convertToFloat(antwortFrame.getPayload())[0]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

    def setInputTypeToBridge_8_75V(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Brueckensensoren mi eienr Speisespannung von 8,75V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x00)

    def setInputTypeToBridge_5V(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Brueckensensoren mi eienr Speisespannung von 5V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x01)

    def setInputTypeToBridge_2_5V(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Brueckensensoren mi eienr Speisespannung von 2,5V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x02)

    def setInputTypeToSingle_Ended(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Single-ended

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x03)

    def setInputTypeToTEMP_PT1000(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Temperatursensor PT1000

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x04)

    def setInputTypeToTemp_K_Type(self, channel):
        '''
        Setzt InputType für den angegeben DMS Kanal
        Fuer Temperatursensor K-Type

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.setInputType(channel, 0x05)

    def setInputType(self, channel, inputType):
        '''
        Setzt InputType für den angegeben DMS Kanal

        :param channel: zugehoeriger DMS-Kanal
        :param InputType: InputType aus Datenblatt
        :type channel: uint8
        :type InputType: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für SetDIOtype
        output = self._gsvLib.buildSetInputTypeGSV8(channel, inputType)

        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()

        # returnstatment erzeugen

        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText()]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())

        return result

    def getInputTypeForBridge_8_75V(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Brueckensensoren mi eienr Speisespannung von 8,75V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x00)

    def getInputTypeForBridge_5V(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Brueckensensoren mi eienr Speisespannung von 8,75V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x01)

    def getInputTypeForBridge_2_5V(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Brueckensensoren mi eienr Speisespannung von 8,75V

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x02)

    def getInputTypeForSingle_Ended(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Signle-ended

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x03)

    def getInputTypeForTemp_PT1000(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Temperatursensor PT1000

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x04)

    def getInputTypeForTemp_K_Type(self, channel):
        '''
        Holt den aktuellen Messbereiche
        Fuer Temperatursensor K-Type

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''

        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0x05)

    def getInputType(self, channel):
        '''
        Sholt den aktuellen Messbereiche

        :param channel: DMS Kanal 1..8 oder 0 für alle
        :type channel: uint8
        :return: AntwortErrorCode und AntwortErrorText
        :rtype: liste
        '''
        # siehe Typen in der Protokollreferenz
        return self.getInputType(channel, 0xFF)

    def getInputType(self, channel, inputType):
        '''
        holt den aktuellen Messbereiche für den angegeben InputType

        :param channel: zugehoeriger DMS-Kanal
        :param InputType: InputType aus Datenblatt
        :type channel: uint8
        :type InputType: uint8
        :return: AntwortErrorCode, AntwortErrorText und Input-Type
        :rtype: liste
        '''

        # erstelle zu sendene Bytefolge für SetDIOtype
        output = self._gsvLib.buildReadInputType(channel, inputType)
        # sende Daten via serialport
        self._gsvSerialPort.write(output)

        # ersten AntwortFrame aus der Queue holen
        antwortFrame = self._antwortQueue.get()
        # returnstatment erzeugen

        if (antwortFrame.getAntwortErrorCode() == 0x00):
            result = [antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText(),self._gsvLib.convertToUint32_t(antwortFrame.getPayload()[1:5])[0]]
        else:
            raise GSV_CommunicationException(antwortFrame.getAntwortErrorCode(), antwortFrame.getAntwortErrorText())
        return result

