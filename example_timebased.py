# -*- coding: utf-8 -*-
"""
Datum 01.2016
@author: ME-Meßsysteme GmbH, Robert Bremsat, Dennis Rump
@version 1.2
"""
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

from gsv8 import gsv8
from datetime import datetime

if __name__ == '__main__':
    # construct device
    # Unix
    dev1 = gsv8("/dev/ttyACM0",115200)
    # Windows
    # dev1 = gsv8("COM26", 115200)
    # dev1 = gsv8("COM26", 115200)

    print "test: " + ' '.join(format(x, '02x') for x in bytearray(dev1.isPinHigh(1)))

    # einen eine Messung anstoßen
    measurement = dev1.ReadValue()
    print 'Kanal 1: {}'.format(measurement.getChannel1())
    print measurement.toString()

    measurement2 = dev1.ReadValue()
    print 'Kanal 1: {}'.format(measurement2.getChannel1())
    print measurement2.toString()

    #dev1.writeDataRate(100.0)
    '''
    dev1.setDIOdirection(9,1);
    dev1.setDIOdirection(10,1);
    dev1.setDIOdirection(1,0);
    dev1.setDIOdirection(2,0);
    dev1.setDIOinitialLevel(1,1);
    dev1.setDIOinitialLevel(2,0);
    dev1.setDIOinitialLevel(10,0);
    dev1.StartTransmission()
    '''

    # dev1.startCSVrecording(10.0, './messungen')

    actTime = lastTime = datetime.now()
    diffTime = actTime - lastTime
    try:
        while(True):
            actTime = datetime.now()
            diffTime = actTime - lastTime
            if(diffTime.seconds >= 0 and diffTime.microseconds>=10000):
                # print datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                # print diffTime
                measurement2 = dev1.ReadValue()
                # print 'Kanal 1: {}'.format(measurement2.getChannel1())
                if(dev1.isPinHigh(9)):
                    # print "JA"
                    dev1.setPinToHigh(1);
                    dev1.setPinToLow(2);
                else:
                    dev1.setPinToHigh(2);
                    dev1.setPinToLow(1);
                    # print "NEIN"
                # print measurement2.toString()
                actTime = lastTime = datetime.now()
            elif (diffTime.seconds > 0):
                actTime = lastTime = datetime.now()
    except KeyboardInterrupt:
        # wennn Programm durch Tastatur beendet wird, Messung stoppen
        dev1.stopCSVrecording()
    finally:
        # destruct device
        dev1 = None
