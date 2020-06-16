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
import threading
import os
import csv
import copy


class CSVwriter(threading.Thread):
    def __init__(self, startTimeStampStr, dictListOfMessungen, csvList_lock, recordPrefix = '', path='./messungen/'):
        threading.Thread.__init__(self)
        self.startTimeStampStr = startTimeStampStr
        self.path = path
        self.recordPrefix = recordPrefix;
        self.filenName = self.path + self.recordPrefix + self.startTimeStampStr + '.csv'
        csvList_lock.acquire()
        self.dictListOfMessungen = copy.deepcopy(dictListOfMessungen)
        csvList_lock.release()

    def run(self):
        if not os.path.exists(self.filenName):
            self.writeHeader = True
        else:
            self.writeHeader = False

        with open(self.filenName, 'a') as csvfile:
            fieldnames = ['timestamp', 'channel0', 'channel1', 'channel2', 'channel3', 'channel4', 'channel5',
                          'channel6', 'channel7']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
 #           try:
            if self.writeHeader:
                headernames = {'timestamp': 'timestamp', 'channel0': 'channel0', 'channel1': 'channel1',
                               'channel2': 'channel2', 'channel3': 'channel3', 'channel4': 'channel4',
                               'channel5': 'channel5', 'channel6': 'channel6', 'channel7': 'channel7'}
                writer.writerow(headernames)
            
            
            writer.writerows(self.dictListOfMessungen)
#            except Exception as e:
#                logging.getLogger('gsv8.router.MessFrameHandler.CSVwriter').critical(
#                    'stopping measurement, can\'t write data! Error: ' + str(e))

            del self.dictListOfMessungen[:]
