#!/usr/bin/env python 

# portable serial port access with python
# this is a wrapper module for different platform implementations
#
# (C) 2001-2010 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

VERSION = '2.7'

import sys
import os

from serial.serialposix import *

