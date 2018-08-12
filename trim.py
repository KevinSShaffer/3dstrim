#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open
from builtins import str
# etc., as needed

from future import standard_library
standard_library.install_aliases()

import sys, io, struct

print("trimming {}".format(sys.argv[1]),)
rom = io.open(sys.argv[1], "rb+")
rom.seek(0x100)
assert  rom.read(4).decode("ascii") == "NCSD"
fullsize = struct.unpack("<I",rom.read(4))[0] << 9
print("from {:,}".format(fullsize),)
rom.seek(0x300)
trimsize = struct.unpack("<I",rom.read(4))[0]
rom.seek(trimsize)
while rom.tell() < fullsize:
    data = rom.read1(1<<16)
    if data == b"": break
    assert min(data) == 0xFF, "{} is not {}".format(min(data), 0xFF)
end = rom.read1(1<<8)
assert end == b"", "{} is not an empty string".format(end)
assert rom.tell() <= fullsize
rom.truncate(trimsize)
rom.close()
print("to {:,} Bytes ({}%)".format(trimsize,(1000*trimsize/fullsize)/10.0))
