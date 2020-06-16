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

import GSV_Exceptions
from GSV6_ErrorCodes import error_code_to_error_shortcut


class BasicFrame:
    frameType = {}
    length_or_channel = {}
    statusbyte = {}
    data = {}

    def __init__(self, data):
        self.data = bytearray(data)
        if len(self.data) < 2:
            raise GSV_Exceptions.GSV6_DataType_Error('BasicFrameType: need more data to construct.')
        self.frameType = (self.data[0] & 0xC0) >> 6
        self.length_or_channel = self.data[0] & 0x0F
        self.statusbyte = self.data[1]
        if len(self.data) < 3:
            self.data = []
        else:
            self.data = self.data[2:]

    def getFrameType(self):
        return self.frameType

    def getLength(self):
        return self.length_or_channel

    def getChannelCount(self):
        return self.length_or_channel

    def getStatusByte(self):
        return self.statusbyte

    def getPayload(self):
        return self.data

    def isMesswertSixAchsisError(self):
        if ((self.statusbyte & 0x02) >> 1) == 1:
            return True
        else:
            return False

    def isMesswertInputOverload(self):
        if (self.statusbyte & 0x01) == 1:
            return True
        else:
            return False

    def getMesswertDataTypeAsString(self):
        type = ((self.statusbyte & 0x70) >> 4)
        if type == 1:
            return 'int16'
        elif type == 2:
            return 'int24'
        elif type == 3:
            return 'float32'
        else:
            return 'unkown'

    def getAntwortErrorCode(self):
        return self.statusbyte

    def getAntwortErrorText(self):
        return error_code_to_error_shortcut.get(self.statusbyte)

    def toString(self):
        if self.frameType == 0:
            # Messwert Frame
            str = 'MesswertFrame: Kanäle: {} Payload: {} Datentype: {}'.format(self.getChannelCount(), ' '.join(
                format(z, '02x') for z in self.data), self.getMesswertDataTypeAsString())
            if self.isMesswertSixAchsisError():
                str += ' !6-Achsen-Fehler!'
            if self.isMesswertInputOverload():
                str += ' !Eingang Übersteuert!'
            return str
        elif self.frameType == 1:
            # Antwort Frame
            str = 'AntwortFrame: Länge des Payloads: {} Fehler: {}'.format(self.getLength(),
                                                                           error_code_to_error_shortcut.get(
                                                                               self.statusbyte))
            if self.length_or_channel > 0:
                str += ' Payload: {}'.format(' '.join(format(z, '02x') for z in self.data))
            return str
        else:
            # error
            return 'unkown FrameType.'
