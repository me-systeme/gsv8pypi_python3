# -*- coding: utf-8 -*-
"""
Datum 02.2016
@author: ME-Meßsysteme GmbH, Robert Bremsat, Dennis Rump
@version 1.2
"""
__author__ = 'Robert bremsat & Dennis Rump'
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
from time import sleep

if __name__ == '__main__':
    # construct device
    # Unix
    dev1 = gsv8("/dev/ttyACM0",230400)
    #dev1 = gsv8("/dev/ttyAMA0",230400)
    # Windows
    # dev1 = gsv8(21, 115200)

    # ausgabetyp setzten
    '''
    result =  dev1.setTXmodefloat()
    if(dev1.isResultOk(result)):
        print "setTXmodefloat erfolgreich"
    '''

    #print('aktuelle Datenrate: {} Hz'.format(dev1.readDataRate()))         # +
    #print('get1wireTempValue: {}'.format(dev1.get1wireTempValue()))        # unknown cmd
    
    """# default
    dev1.setDIOdirection(1,1)           # +
    dev1.setDIOdirection(2,0)           # +
    dev1.setDIOdirection(3,0)           # +
    dev1.setDIOdirection(4,0)           # +
    """
    """
    for i in range(1,5):
        print('getDIOdirection, group {}: {}'.format(i, dev1.getDIOdirection(i)))           # +
        sleep(0.1)
        dev1.setDIOdirection(i,0)           # +
        sleep(0.1)
        print('getDIOdirection, group {}: {}'.format(i, dev1.getDIOdirection(i)))           # +
        sleep(0.1)
        dev1.setDIOdirection(i,1)           # +
        sleep(0.1)
        print('getDIOdirection, group {}: {}'.format(i, dev1.getDIOdirection(i)))           # +
        dev1.setDIOgroupToOutput(i)           # +
        print('getDIOdirection, group {}: {}'.format(i, dev1.getDIOdirection(i)))           # +
        dev1.setDIOgroupToInput(i)           # +
        print('getDIOdirection, group {}: {}'.format(i, dev1.getDIOdirection(i)))           # +
    """
    
    """
    # set initial level of DIO 1 to high and low
    print('getDIOinitialLevel: {}'.format(dev1.getDIOinitialLevel(1)))     # +
    dev1.setDIOinitialLevel(1,1)
    print('getDIOinitialLevel: {}'.format(dev1.getDIOinitialLevel(1)))     # +
    dev1.setDIOinitialLevel(1,0)
    print('getDIOinitialLevel: {}'.format(dev1.getDIOinitialLevel(1)))     # +

    # set level of DIO 1 to low and high
    # beinhaltet auch Tests für: setPinToHigh, setPinToLow
    print('getDIOlevel: {}'.format(dev1.getDIOlevel(1)))     # +
    dev1.setDIOlevel(1,1)
    print('getDIOlevel: {}'.format(dev1.getDIOlevel(1)))     # +
    dev1.setDIOlevel(1,0)
    print('getDIOlevel: {}'.format(dev1.getDIOlevel(1)))     # +
    """
    
    """
    # beinhaltet auch den Test für: setDIOtype, setOutputHighByThreshold, setOutputLowByThreshold
    # setOutputHighIfOutsideWindow, setOutputLowIfOutsideWindow, setPinTypeToInpu, setPinTypeTOutput
    # setStartTransmissionByInputIsHigh
    dev1.setDIOtoGenralPurposeInput(1)
    dev1.setDIOtoGenralPurposeOutput(1)
    """
    
    


    """
    for i in range(1,17):
        #print('getDIOtype, Pin{}: {}'.format(i, dev1.getDIOtype(i)))        # +
        #print('isPinHigh, Pin{}: {}'.format(i, dev1.isPinHigh(i)))          # +
        #print('isPinLow, Pin{}: {}'.format(i, dev1.isPinLow(i)))            # +
        #for k in range(0,2):
        #    print('readDIOthreshold, Pin{}, level{}: {}'.format(i, k, dev1.readDIOthreshold(i,k)))            # +
        print('readLowerDIOthreshold, Pin{}: {}'.format(i, dev1.readLowerDIOthreshold(i)))            # +
        print('readUpperDIOthreshold, Pin{}: {}'.format(i, dev1.readUpperDIOthreshold(i)))            # +
    """
    print('readLowerDIOthreshold: {}'.format(dev1.readLowerDIOthreshold(1)))            # +
    dev1.writeLowerDIOthreshold(1, -2.1)                                                # +
    print('readLowerDIOthreshold: {}'.format(dev1.readLowerDIOthreshold(1)))            # +
    print('readUpperDIOthreshold: {}'.format(dev1.readUpperDIOthreshold(1)))            # +
    dev1.writeUpperDIOthreshold(1, 2.1)                                                 # +
    print('readUpperDIOthreshold: {}'.format(dev1.readUpperDIOthreshold(1)))            # +
    
    """
    for i in range(1,9):
        #print('getInputType: {}'.format(dev1.getInputType(i)))                 # fehlendes Argument
        print('getInputTypeForBridge_2_5V, ch.{}: {}'.format(i, dev1.getInputTypeForBridge_2_5V(i))) 
        print('getInputTypeForBridge_5V, ch.{}: {}'.format(i, dev1.getInputTypeForBridge_5V(i))) 
        print('getInputTypeForBridge_8_75V, ch.{}: {}'.format(i, dev1.getInputTypeForBridge_8_75V(i))) 
        print('getInputTypeForSingle_Ended, ch.{}: {}'.format(i, dev1.getInputTypeForSingle_Ended(i))) 
        print('getInputTypeForTemp_K_Type, ch.{}: {}'.format(i, dev1.getInputTypeForTemp_K_Type(i))) 
        print('getInputTypeForTemp_PT1000, ch.{}: {}'.format(i, dev1.getInputTypeForTemp_PT1000(i))) 
    """
    """
    print('getInputTypeForBridge_2_5V, ch.1: {}'.format(dev1.getInputType(1, 0xFF))) 
    dev1.setInputTypeToBridge_5V(1)
    print('getInputTypeForBridge_2_5V, ch.1: {}'.format(dev1.getInputType(1, 0xFF))) 
    """
    
    #print('getInputTypeForBridge_2_5V, ch.1: {}'.format(dev1.getInputTypeForBridge_2_5V(1))) 

    #print('isDIOgroupInput: {}'.format(dev1.isDIOgroupInput(0)))     # +
    #print('isDIOgroupOutput: {}'.format(dev1.isDIOgroupOutput(0)))     # +

    """
    print('isSixAxisMatrixActive: {}'.format(dev1.isSixAxisMatrixActive()))     # +
    dev1.setSixAxisMatrixActive(True)                                           # keine Antwort
    print('isSixAxisMatrixActive: {}'.format(dev1.isSixAxisMatrixActive()))     # +
    """
    
    #dev1.setTXmodefloat()  # ERR: 0x52 - Die Daten eines Datenparameters sind falsch
    #dev1.setUserScaleBySensor(1, 2.5, 1.0)     # +
    #dev1.startCSVrecording(10.0, "./messungen/")   # +
    
    # destruct device
    dev1 = None
