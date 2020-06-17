# -*- coding: utf-8 -*-
"""
Datum 01.2016
@author: ME-Meßsysteme GmbH, Dennis Rump
@version 1.2
"""

__author__ = 'Dennis Rump'
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

from gsv8 import gsv8
import signal
import sys

if __name__ == '__main__':
    # construct device
    # Unix
    dev1 = gsv8("/dev/ttyACM0",115200)
    # Windows
    # dev1 = gsv8(21, 115200)

    schwellwert1 = 10.0
    hysterese_high = 7.0
    hysterese_low = 5.0


    # einen eine Messung anstoßen
    measurement = dev1.ReadValue()
    print('Kanal 1: {}'.format(measurement.getChannel1()))
    print(measurement.toString())

    measurement2 = dev1.ReadValue()
    print('Kanal 1: {}'.format(measurement2.getChannel1()))
    print(measurement2.toString())

    print('is Pin 1 high?: {}'.format(dev1.isPinHigh(1)))
    print('is Pin 2 low?: {}'.format(dev1.isPinLow(2)))

    # ist die Verrechnungsmatrix aktiv?
    if (dev1.isSixAxisMatrixActive()):
        print("matrix active")
    else:
        print("matrix inactive")

    dev1.StartTransmission()

    try:
        while (True):
            # Eine Messung anfordern und Messwert von Kanal1 in einer Variablen speichern
            messwert = dev1.ReadValue().getChannel7()
            # print messwert
            '''
            # Aktion auf Schwellwert - Enifache Variante
            if(messwert >= schwellwert1):
                dev1.startCSVrecordingWithoutStartTransmisson('./messungen')
            else:
                 dev1.stopCSVrecordingWithoutStopTransmission()
            '''

            # Aktion auf Schwellwert - mit Hysterese
            if(messwert >= hysterese_high):
                dev1.startCSVrecordingWithoutStartTransmisson('./messungen', 'dev1_')
            elif(messwert <= hysterese_low):
                dev1.stopCSVrecordingWithoutStopTransmission()
    except KeyboardInterrupt:
        dev1.stopCSVrecording()
    finally:
        # destruct device
        dev1 = None
