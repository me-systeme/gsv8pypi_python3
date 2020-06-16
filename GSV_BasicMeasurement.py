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

class BasicMeasurement:
    """

    Die Klasse stellt eine Basis Messobjekt zur Verfügung.

    Es werden getter und setter Methoden für die einzelnen Kanäle, des Timestamps, des inputoverloads und des SixAxisErrors bereitgestellt

    """

    data = []

    def __init__(self, data):
        self.data = data

    '''
        Die Methode getTimestamp returned einen Zeitstempel, der zum eintreffen des Messwerts erzeugt wurde.
    '''
    def getTimestamp(self):
        return self.data[0]

    '''
        Die Methode getChannel0 returned des messwert von Kanal 0
    '''
    def getChannel1(self):
        if(len(self.data[1])>=1):
            return self.data[1]['channel0']

    '''
        Die Methode getChannel1 returned des messwert von Kanal 1
    '''
    def getChannel2(self):
        if(len(self.data[1])>=2):
            return self.data[1]['channel1']

    '''
        Die Methode getChannel2 returned des messwert von Kanal 2
    '''
    def getChannel3(self):

        if(len(self.data[1])>=3):
            return self.data[1]['channel2']

    '''
        Die Methode getChannel3 returned des messwert von Kanal 3
    '''
    def getChannel4(self):
        if(len(self.data[1])>=4):
            return self.data[1]['channel3']

    '''
        Die Methode getChannel4 returned des messwert von Kanal 4
    '''
    def getChannel5(self):
        if(len(self.data[1])>=5):
            return self.data[1]['channel4']

    '''
        Die Methode getChannel5 returned des messwert von Kanal 5
    '''
    def getChannel6(self):
        if(len(self.data[1])>=6):
            return self.data[1]['channel5']

    '''
        Die Methode getChannel6 returned des messwert von Kanal 6
    '''
    def getChannel7(self):
        if(len(self.data[1])>=7):
            return self.data[1]['channel6']

    '''
        Die Methode getChannel7 returned des messwert von Kanal 7
    '''
    def getChannel8(self):
        if(len(self.data[1])>=8):
            return self.data[1]['channel7']

    '''
        Die Methode isInputOverload returned den InputOverload Status
    '''
    def isInputOverload(self):
        return self.data[2]

    '''
        Die Methode isInputOverload returned den SixAxisError Status
    '''
    def isSixAxisError(self):
        return self.data[3]

    def toString(self):
        str = 'Timestamp: {}; Messwerte: Kanal0: {}; Kanal1: {}; Kanal2: {};Kanal3: {}; Kanal4: {}; Kanal5: {};nKanal6: {}; Kanal7: {};InputOverload: {}; SixAxisError: {}'.format(
            self.getTimestamp(), self.getChannel1(), self.getChannel2(), self.getChannel3(), self.getChannel4(),
            self.getChannel5(), self.getChannel6(), self.getChannel7(), self.getChannel8(), self.isInputOverload(),
            self.isSixAxisError())
        return str
