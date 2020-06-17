# -*- coding: utf-8 -*-
"""
Datum 02.2016
@author: ME-Meßsysteme GmbH, Dennis Rump
@version 1.2
"""
__author__ = 'Dennis Rump'
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2016 ME-Meßsysteme GmbH
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

if __name__ == '__main__':
    # construct device
    # Unix
    dev1 = gsv8("/dev/ttyACM0",230400)
    # Windows
    # dev1 = gsv8(21, 115200)

    # Datenrate setzten
    result = dev1.writeDataRate(50.0)
    # Ergebnis pruefen
    if(dev1.isResultOk(result)):
        print("writeDataRate erfolgreich")

    # datenrate veraendern
    print('aktuelle Datenrate: {} Hz'.format(dev1.readDataRate()))

    # DIO Gruppe 1 als Input Konfigurieren ( IOPin 1..4 (1.1 - 1.4) )
    result = dev1.setDIOgroupToInput(1)
    # Ergebnis pruefen
    if(dev1.isResultOk(result)):
        print("setDIOgroupToInput  fuer Gruppe 1 erfolgreich")

    # DIO Gruppe 2 als Output Konfigurieren ( IOPin 5..8 (2.1 - 2.4) )
    result = dev1.setDIOgroupToOutput(2)
    # Ergebnis pruefen
    if(dev1.isResultOk(result)):
        print("setDIOgroupToOutput fuer Gruppe 2 erfolgreich")

    # DIO Gruppe 3 als Output Konfigurieren ( IOPin 9..12 (3.1 - 3.4) )
    result = dev1.setDIOgroupToOutput(3)
    # Ergebnis pruefen
    if(dev1.isResultOk(result)):
        print("setDIOgroupToOutput fuer Gruppe 3 erfolgreich")

    # DIO Gruppe 4 als Out Konfigurieren ( IOPin 13..16 (4.1 - 4.4) )
    result = dev1.setDIOgroupToOutput(4)
    # Ergebnis pruefen
    if(dev1.isResultOk(result)):
        print("setDIOgroupToOutput  fuer Gruppe 4 erfolgreich")


    dev1.setInputToTaraInputForAllChannels(3);
    #dev1.setStartTransmissionByInputIsHigh(4);
    dev1.setDIOtoGenralPurposeInput(4);

    # Nun reaktion auf die Schwellwerte konfigurieren
    # IOPin 9 (3.1) soll auf Kanal 1 reagieren
    dev1.setOutputHighIfInsideWindow(9,7)
    # IOPin 10 (3.2) soll auf Kanal 2 reagieren
    dev1.setOutputHighIfOutsideWindow(10,2)
    # IOPin 11 (3.3) soll auf Kanal 3 reagieren
    dev1.setOutputHighIfOutsideWindow(11,3)
    # IOPin 12 (3.4) soll auf Kanal 4 reagieren
    dev1.setOutputHighIfOutsideWindow(12,4)
    # IOPin 13 (4.1) soll auf Kanal 5 reagieren
    dev1.setOutputHighIfOutsideWindow(13,5)
    # IOPin 14 (4.2) soll auf Kanal 6 reagieren
    dev1.setOutputHighIfOutsideWindow(14,6)
    # IOPin 15 (4.3) soll auf Kanal 1 reagieren
    dev1.setOutputHighIfInsideWindow(15,7)
    # IOPin 16 (4.4) soll auf Kanal 7 reagieren
    dev1.setOutputHighIfOutsideWindow(16,7)

    # lesen und schreiben des oberen oder unteren Schwellwertes
    print('unterer Schwellwert fuer DMS-Kanal 1: {}'.format(dev1.readLowerDIOthreshold(9)))
    print('oberer  Schwellwert fuer DMS-Kanal 1: {}'.format(dev1.readUpperDIOthreshold(9)))

    # Schwellwerte fuer Fx
    dev1.writeLowerDIOthreshold(9,+5.0)
    dev1.writeUpperDIOthreshold(9,+40.0)
    # Schwellwerte fuer Fy
    dev1.writeLowerDIOthreshold(10,-250.0)
    dev1.writeUpperDIOthreshold(10,+250.0)
    # Schwellwerte fuer Fz
    dev1.writeLowerDIOthreshold(11,-1000.0)
    dev1.writeUpperDIOthreshold(11,+1000.0)

    # Schwellwerte fuer Mx
    dev1.writeLowerDIOthreshold(12,-10.0)
    dev1.writeUpperDIOthreshold(12,+10.0)
    # Schwellwerte fuer My
    dev1.writeLowerDIOthreshold(13,-10.0)
    dev1.writeUpperDIOthreshold(13,+10.0)
    # Schwellwerte fuer Mz
    dev1.writeLowerDIOthreshold(14,-10.0)
    dev1.writeUpperDIOthreshold(14,+10.0)

    # Schwellwerte fuer Mz
    dev1.writeLowerDIOthreshold(15,+5.0)
    dev1.writeUpperDIOthreshold(15,+40.0)

    # Schwellwerte fuer DMS Kanal 7
    dev1.writeLowerDIOthreshold(16,-2500.0)
    dev1.writeUpperDIOthreshold(16,+2500.0)


    # Verrechnungsmatrix aktivieren
    if(dev1.setSixAxisMatrixActive(True)):
        pass
        # aktiverung/deaktivierung erflgreich

    if(dev1.isSixAxisMatrixActive()):
        print("matrix active")
    else:
        print("matrix inactive")

    # destruct device
    dev1 = None
