##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2016 Vladimir Ermakov <vooon341@gmail.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
##

import sigrokdecode as srd
from functools import reduce

class SamplerateError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 3
    id = 'rinnai'
    name = 'Rinnai'
    longname = 'Rinnai decoder'
    desc = 'Rinnai protocol.'
    license = 'gplv3+'
    inputs = ['logic']
    outputs = ['rinnai']
    channels = (
        {'id': 'rx', 'name': 'Rx', 'desc': 'Rx data line'},
    )
    annotations = (
        ('bit', 'Bit'),
        ('reset', 'RESET'),
        ('code', 'CODE'),
    )
    annotation_rows = (
        ('bit', 'Bits', (0, 1)),
        ('code', 'CODE', (2, )),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplerate = None
        self.oldpin = None
        self.ss_packet = None
        self.ss = None
        self.es = None
        self.bits = []
        self.inreset = False

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value

    def handle_bits(self, samplenum):
        if self.ss_packet is None:
            return
        if len(self.bits) == 48:
            self.put(self.ss_packet, samplenum, self.out_ann, [2, ['#%48s' % self.bits]])

    def decode(self):
        if not self.samplerate:
            raise SamplerateError('Cannot decode without samplerate.')

        while True:
            # TODO: Come up with more appropriate self.wait() conditions.
            (pin,) = self.wait()

            if self.oldpin is None:
                self.oldpin = pin
                self.ss = self.samplenum
                continue

            if self.oldpin != pin:
                tH = (self.samplenum - self.ss) / self.samplerate
                
                if not pin and tH > 0.00065:
                    self.put(self.ss, self.samplenum, self.out_ann, [1, ['HEAD', 'HED', 'H']])
                    self.ss_packet = self.ss
                    self.bits = []

                elif tH < 0.00055 and tH > 0.0002:
                    self.bits.append(self.oldpin)
                    self.put(self.ss, self.samplenum, self.out_ann, [0, ['%d' % self.oldpin]])
                    self.handle_bits(self.samplenum)

                self.ss = self.samplenum
            
            self.oldpin = pin
