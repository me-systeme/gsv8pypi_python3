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

error_code_to_error_shortcut = {
    0x00: 'ERR_OK',
    0x01: 'ERR_OK_CHANGED',

    0x40: 'ERR_CMD_NOTKNOWN',
    0x41: 'ERR_CMD_NOTIMPL',
    0x42: 'ERR_FRAME_ERROR',

    0x50: 'ERR_PAR',
    0x51: 'ERR_PAR_ADR',
    0x52: 'ERR_PAR_DAT',
    0x53: 'ERR_PAR_BITS',
    0x54: 'ERR_PAR_ABSBIG',
    0x55: 'ERR_PAR_ABSMALL',
    0x56: 'ERR_PAR_COMBI',
    0x57: 'ERR_PAR_RELBIG',
    0x58: 'ERR_PAR_RELSMALL',
    0x59: 'ERR_PAR_NOTIMPL',
    0x5A: 'ERR_PAR_TIMEOUT',
    0x5B: 'ERR_WRONG_PAR_NUM',
    0x5C: 'ERR_PAR_NOFIT_SETTINGS',
    0x5E: 'ERR_MEMORY_WRONG_COND',
    0x5F: 'ERR_MEMORY_ACCESS_DENIED',

    0x70: 'ERR_ACC_DEN',
    0x71: 'ERR_ACC_BLK',
    0x72: 'ERR_ACC_PWD',
    0x74: 'ERR_ACC_MAXWR',
    0x75: 'ERR_ACC_PORT',

    0x80: 'ERR_INTERNA',
    0x81: 'ERR_ARITH',
    0x82: 'ERR_INTER_ADC',
    0x83: 'ERR_MWERT_ERR',
    0x84: 'ERR_EEPROM',

    0x91: 'ERR_RET_TXBUF',  # wie geht das denn?
    0x92: 'ERR_RET_BUSY',
    0x99: 'ERR_RET_RXBUF'
}

error_codes_to_messages_DE = {
    0x00: 'Kommando ohne Fehler ausgeführt.',
    0x01: 'Kommando  ohne  Fehler  ausgeführt,  Parameter wurden geändert.',

    0x40: 'Das Kommando ist unbekannt.',
    0x41: 'Das  Kommando  ist  bekannt,  wird  jedoch  nicht  unterstützt.  Es  kann  sich  hier  um  Kommandos  handeln, die für den Gerätetypen GSV-6 nicht vorgesehen sind.',
    0x42: 'Der Frame des Kommandos ist falschaufgebaut.',  # Frame-Parse error

    0x50: 'Ein falscher Parameter wurde übergeben.',
    0x51: 'Der übergebene Index oder die Adresse ist falsch.',
    0x52: 'Die Daten eines Datenparameters sind falsch.',
    0x53: 'Falsche Bits im Parameter.',
    0x54: 'Der Absolutwert eines Parameters ist zu groß.',
    0x55: 'Der Absolutwert eines Parameters ist zu klein.',
    0x56: 'Die Parameter Kombination ist Fehlerhaft.',
    0x57: 'Ein  Parameter  ist  in  Relation  zu  den  anderen  zu groß.',
    0x58: 'Ein  Parameter  ist  in  Relation  zu  den  anderen  zu klein.',
    0x59: 'Das Kommando unterstützt den Parameter nicht.',
    0x5A: 'Die Parameter zum Kommando sind nicht innerhalb von 200 ms eingetroffen.',
    0x5B: 'Die  Anzahl  der  Parameter  passt  nicht  zum  Kommando.  Bits  3~0  im  ersten  Byte  des  Kommando Blocks zu hoch bzw. niedrig.',
    0x5E: 'Speicherzugriff Bedingung nicht erfüllt.',
    0x5F: 'Speicher Zugriff verweigert.',

    0x70: 'Kommando wird nicht ausgeführt, weil die Berechtigung fehlt.',
    0x71: 'Kommando wurde nicht ausgeführt, da Blocking gesetzt wurde.',
    0x72: 'Passwort falsch oder nicht vorhanden.',
    0x74: 'Die Maximale Anzahl der Ausführungen ist überschritten.',
    0x75: 'Keine Schreibrechte auf dem Port.',

    0x80: 'Interner Ausnahmefehler.',
    0x81: 'Interner arithmetischer Fehler.',
    0x82: 'Fehlerhaftes Verhalten des ADC.',
    0x83: 'Fehler im Messwert.',
    0x84: 'Fehler im EEPROM.',

    0x91: 'Sendepuffer Überlauf.',  # wie geht das denn?
    0x92: 'Die CPU ist ausgelastet.',
    0x99: 'Der Empfangspuffer ist voll.'
}
