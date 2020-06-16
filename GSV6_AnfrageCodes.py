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

anfrage_code_to_shortcut = {
    'GetInterface': 0x01,
    'ReadZero': 0x02,
    'WriteZero': 0x03,
    'ReadAoutOffset': 0x04,
    'WriteAoutOffset': 0x05,
    'ReadAoutScale': 0x06,
    'WriteAoutScale': 0x07,
    'SaveAll': 0x0A,
    'SetZero': 0x0C,
    'ReadUserScale': 0x14,
    'WriteUserScale': 0x15,
    'StartTransmission': 0x24,
    'StopTransmission': 0x23,
    'GetSerialNo': 0x1F,
    'GetUnitText': 0x11,
    'SetUnitText': 0x12,
    'GetUnitNo': 0x0F,
    'SetUnitNo': 0x10,
    'MEsetID': 0x19,
    'GetMode': 0x26,
    'SetMode': 0x27,
    'GetFirmwareVersion': 0x2B,
    'GetDeviceHours': 0x56,
    'MEwriteInputRange': 0x34,
    'GetValue': 0x3B,
    'GetDIOdirection': 0x59,
    'SetDIOdirection': 0x5A,
    'GetDIOtype': 0x5B,
    'SetDIOtype': 0x5C,
    'GetDIOlevel': 0x5D,
    'SetDIOlevel': 0x5E,
    'ReadDIOthreshold': 0x5F,
    'WriteDIOthreshold': 0x60,
    'GetDIOinitialLevel': 0x61,
    'SetDIOinitialLevel': 0x62,
    'Get1WireTempValue': 0x79,
    'ReadDataRate': 0x8A,
    'GetTXMode': 0x80,
    'SetTXMode': 0x81,
    'WriteDataRate': 0x8B,
    'ReadUserOffset': 0x9A,
    'WriteUserOffset': 0x9B,
    'GetInputType': 0xA2,
    'SetInputType': 0xA3
}
