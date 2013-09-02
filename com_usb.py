#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# USB comunication
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import usb

ROBO_USB_VENDOR_ID      = 0x146a
ROBO_IF_USB_PRODUCT_ID  = 0x0001
ROBO_IOE_USB_PRODUCT_ID = 0x0002
ROBO_RFD_USB_PRODUCT_ID = 0x0003
ROBO_SAL_USB_PRODUCT_ID = 0x0005 # sound + lights

ROBO_CONFIGURATION = 1
ROBO_INTERFACE     = 0

#esto no es al reves?
ROBO_IF_OUT_EP = 0x01
ROBO_IF_IN_EP  = 0x81

TIMEOUT = 250

ERROR = -1



class usb_device():

    def __init__(self, dev):
        self.dev = dev
        self.debug = False

    def _debug(self, message, err=''):
        if self.debug:
            print message, err

    def open_device(self):
        """
        Open the device, configure the interface
        """
        try:
            if self.dev.is_kernel_driver_active(ROBO_INTERFACE):
                self.dev.detach_kernel_driver(ROBO_INTERFACE)
            self.dev.set_configuration(ROBO_CONFIGURATION)
        except usb.USBError, err:
            self._debug('ERROR:com_usb:open_device', err)
            raise

    def close_device(self):
        """
        Close the comunication
        """
        self.dev = None

    def read(self, size):
        """
        Read from the device length bytes
        """
        try:
            return self.dev.read(ROBO_IF_OUT_EP, size, ROBO_INTERFACE, TIMEOUT)
        except Exception, err:
            self._debug('ERROR:com_usb:read', err)
            raise
 
    def write(self, data):
        """
        Write in the device: data
        """
        try:
            return self.dev.write(ROBO_IF_IN_EP, data, ROBO_INTERFACE, TIMEOUT)
        except Exception, err:
            self._debug('ERROR:com_usb:write', err)
            raise

    def get_address(self):
        """
        Get unique address for the usb
        """
        if self.dev is not None:
            return self.dev.address
        else:
            return None

def find():
    """
    List all busses and returns a list of baseboards detected
    """
    l = []
    for b in usb.core.find(find_all=True, idVendor=ROBO_USB_VENDOR_ID):
        l.append(usb_device(b))
    return l

