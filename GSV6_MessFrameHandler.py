# -*- coding: utf-8 -*-
__author__ = 'Dennis Rump'
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Dennis Rump
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

import logging
from datetime import datetime
import os
import threading
from CSVwriter import CSVwriter
from GSV_Exceptions import GSV_FilepathException


class MessFrameHandler():
    """

   Die Klasse MessFrameHandler verarbeite neue MesswertFrames und fügt diese zur der double-ended queue hinzu.

   """

    # def __init__(self, messertRotatingQueue, gsv_lib):
    def __init__(self, lastMesswert, gsv_lib):
        # self.messertRotatingQueue = messertRotatingQueue
        self.lastMesswert = lastMesswert
        self.gsv_lib = gsv_lib
        self.safeOption = False
        self.messCSVDictList = []
        self.messCSVDictList_lock = threading.Lock()
        self.maxCacheMessCount = 10
        self.startTimeStampStr = ''
        self.recordPrefix = ''
        self.doRecording = False
        self.messCounter = 0

    def computeFrame(self, frame):
        '''
        Die Methode computeFrame erhält einen vollständigen Frame als basicFrameType und extrahiert die Messwerte der einzelnen Kanäle
        '''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        measuredValues = bytearray(frame.getPayload())
        values = self.gsv_lib.convertToFloat(measuredValues)

        measuredValues = {}
        counter = 0
        for f in values:
            # there is no append/add function for Python Dictionaries
            measuredValues['channel' + str(counter)] = f
            counter += 1
        if frame.isMesswertInputOverload():
            inputOverload = True
        else:
            inputOverload = False
        if frame.isMesswertSixAchsisError():
            sixAxisError = True
        else:
            sixAxisError = False

        if self.doRecording:
            # handle CSVwrting
            self.messCounter += 1
            # add data here
            self.messCSVDictList_lock.acquire()

            tmpM = {'timestamp': timestamp}
            for (i, value) in enumerate(values):
                tmpM['channel'+str(i)] = value
            self.messCSVDictList.append(tmpM)
            '''
            self.messCSVDictList.append(
                {'timestamp': timestamp, 'channel0': values[0], 'channel1': values[1], 'channel2': values[2],
                 'channel3': values[3], 'channel4': values[4], 'channel5': values[5], 'channel6': values[6],
                 'channel7': values[7]})
            '''
            self.messCSVDictList_lock.release()
            if (self.messCounter >= self.maxCacheMessCount):
                self.messCounter = 0
                # semaphore lock?
                self._writeCSVdataNow()
                del self.messCSVDictList[:]

        # add new measure data to queue
        measureData = [timestamp, measuredValues, inputOverload, sixAxisError]
        # self.messertRotatingQueue.append(measureData)
        self.lastMesswert.setVar(measureData)
        logging.getLogger('gsv8.FrameRouter.MessFrameHandler').debug('Received MessFrame added.')

    def startRecording(self, filePath, prefix):
        if(self.doRecording):
            return
        logging.getLogger('gsv8.FrameRouter.MessFrameHandler').info('Messung gestartet.')
        # check file path
        self.csvpath = filePath
        if self.csvpath[-1] != '/':
            self.csvpath += '/'
        if not os.path.exists(self.csvpath):
            raise GSV_FilepathException(file, 'Bad Filepath; Filepath doesn\'t exists')
        else:
            # set timestamp
            self.startTimeStampStr = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            self.recordPrefix = prefix
            self.doRecording = True

    def stopRecording(self):
        if self.doRecording:
            logging.getLogger('gsv8.FrameRouter.MessFrameHandler').info('Messung gestopt.')
            if (len(self.messCSVDictList) > 0):
                self._writeCSVdataNow()
            del self.messCSVDictList[:]
        self.doRecording = False

    def _writeCSVdataNow(self):
        # start csvWriter
        writer = CSVwriter(self.startTimeStampStr, self.messCSVDictList, self.messCSVDictList_lock, self.recordPrefix, self.csvpath)
        writer.start()
