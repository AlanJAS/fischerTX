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

import time

RETARDO = 2

t1 = [0x02,0x55,0x00,0x14,
      0x02,0x00,0x00,0x00, #FROM
      0x01,0x00,0x00,0x00, #TO
      0x01,0x00,0x00,0x00, #TID SID
      0x01,0x00,0x00,0x00, #COMMAND
      0x00,0x00,0x00,0x00, #DATA
      0xff,0xe7,0x03]

t2 = [0x02,0x55,0x00,0x18,
      0x02,0x00,0x00,0x00, #FROM
      0x01,0x00,0x00,0x00, #TO
      0x02,0x00,0x01,0x00, #TID SID
      0x06,0x00,0x00,0x00, #COMMAND
      0x01,0x00,0x00,0x00, #DATA
      0x00,0x00,0x00,0x00,
      0xff,0xdb,0x03]

t3 = [0x02,0x55,0x00,0x18,
      0x02,0x00,0x00,0x00, #FROM
      0x01,0x00,0x00,0x00, #TO
      0x03,0x00,0x01,0x00, #TID SID
      0x07,0x00,0x00,0x00, #COMMAND
      0x01,0x00,0x00,0x00, #DATA
      0x00,0x00,0x00,0x00,
      0xff,0xd9,0x03]

t4 = [0x0d,0x67,0x65,0x74,0x5f,0x73,0x65,0x72,0x5f,0x6e,0x75,0x6d,0x0d]

#win 9e
#linux a2

t5 = [0x02,0x55,0x00,0x48,
      0x02,0x00,0x00,0x00, #FROM
      0x01,0x00,0x00,0x00, #TO
      0x01,0x00,0x00,0x00, #TID SID
      0x05,0x00,0x00,0x00, #COMMAND
      0x01,0x00,0x00,0x00, #DATA
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x81,0x81,0x81,0x81,
      0x81,0x81,0x81,0x81,
      0x01,0x01,0x01,0x01,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,
      0xfb,0xa2,0x03]

#segunda linea del 5
#0x05,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01,

p6 = [0x02,0x55,0x00,0x44,
      0x02,0x00,0x00,0x00, #FROM
      0x01,0x00,0x00,0x00, #TO
      0x02,0x00,0x02,0x00, #TID SID
      0x02,0x00,0x00,0x00, #COMMAND
      0x01,0x00,0x00,0x00] #DATA



t6 = p6 + [0] * 48 + [0xff, 0xb2, 0x03]

t7 = p6 + [0] * 48 + [0xff, 0xb2, 0x03]



FISCHER_VENDOR_ID  = 0x221d
FISCHER_PRODUCT_ID = 0x1000

ROBO_CONFIGURATION = 1
ROBO_INTERFACE     = 1


ROBO_IF_OUT_EP = 0x82
ROBO_IF_IN_EP  = 0x03

TIMEOUT = 1000

ERROR = -1



class usb_device():

    def __init__(self, dev):
        self.dev = dev
        self.debug = False

    def _debug(self, message, err=''):
        if self.debug:
            print message, err

    def open_device(self):
        if self.dev.is_kernel_driver_active(ROBO_INTERFACE):
            print 'module active, detach'
            self.dev.detach_kernel_driver(ROBO_INTERFACE)
        self.dev.set_configuration(ROBO_CONFIGURATION)
        # why?
        self.dev.reset()

    def close_device(self):
        self.dev = None

    def read(self, size=128):
        try:
            return self.dev.read(ROBO_IF_OUT_EP, size, TIMEOUT)
        except Exception, err:
            print err
            return []
 
    def write(self, data):
        #print '****************************************************************'
        print 'writting..', data
        h, l = self.calculate_CRC(data)
        data[-3] = h
        data[-2] = l
        return self.dev.write(ROBO_IF_IN_EP, data, TIMEOUT)


    def get_address(self):
        if self.dev is not None:
            return self.dev.address
        else:
            return None

    def get_info(self):
        try:
            names = usb.util.get_string(self.dev, 255, 1, None).encode('ascii')
            copy = usb.util.get_string(self.dev, 255, 2, None).encode('ascii')
            sn = usb.util.get_string(self.dev, 255, 3, None).encode('ascii')
            return [names, copy, sn]
        except Exception, err:
            self._debug('ERROR:com_usb:get_info', err)
            raise

    def get_serial_number(self):
        print 'getting serial number...'
        b.write(t4)
        time.sleep(RETARDO)
        # 59 bytes?
        l = b.read()
        print l
        if len(l) > 41:
            
            serie = ''.join(chr(s) for s in l[31:41])
            print "Serial:", serie
            return serie
        return ''

    def get_name(self):
        print 'getting name...'
        b.write(t4)
        l = b.read()
        print l
        name = ''
        if len(l) > 41:
            name = l[2:13]
            name = ''.join(s for s in name)
            print name
            return name
        return ''  

    def get_mac_address(self):
        print 'getting mac address...'
        b.write(t2)
        ret = b.read(128)
       
        test = ""
        for c in ret[28:40]:
            test = test + chr(c)

        print "Name:", test

        test = ""
        for c in ret[40:62]:
            test = test + chr(c)

        print "Mac:", test


    def update_byte(self, b, o1, o2):
        global t2, t3, t6
        
        t2[14] = b
        t3[14] = b

        t2[29] = o1
        t3[29] = o2

        t7[14] = b + 1


    def calculate_CRC(self, msg):
        s = 0
        msg = msg[2:-3]
        for b in msg:
            s = s + b
        c = 65535 - s + 1
        h = c / 256
        l = c % 256
        return h, l

def find():
    """
    List all busses and returns a list of baseboards detected
    """
    l = []
    for b in usb.core.find(find_all=True, idVendor=FISCHER_VENDOR_ID, idProduct=FISCHER_PRODUCT_ID):
        l.append(usb_device(b))
    return l



if __name__ == "__main__":
    print len(t1), t1
    print len(t2), t2
    print len(t3), t3
    print len(t4), t4
    print len(t5), t5
    print len(t6), t6
    
    print "\n\n"

    l = find()
    b = l[0]

    print 'opening...'
    b.open_device()


    time.sleep(RETARDO)
    print 'primer mensaje'
    b.write(t1)
    
    first = b.read()
    print 'len first', len(first)
    if len(first) > 14:
        print first
        ff = first[14]
        print 'first',  ff
        
        mn = first[25]
        ts1 = (mn + 0x5a) % 256
        ts2 = (mn + 0x58) % 256
        b.update_byte(ff, ts1, ts2)
        
 

    time.sleep(RETARDO)
    b.get_mac_address()


    b.write(t3)
    
    print b.read()

    time.sleep(RETARDO)
    b.get_serial_number()

    
    print 'quinto'
    time.sleep(RETARDO)
    b.write(t5)
    
    time.sleep(RETARDO)
    print 'leyendo 5..'
    ret =  b.read()
    print ret
    print 'hay que mandar', ret[14] + 2, hex(ret[14] + 2)

    t6[14] = ret[14] + 2

    print 'el especial', ret[-2]
    t6[-2] = ret[-2] + 0x3b
    
    time.sleep(RETARDO) 



    print 'sexto'
    b.write(t6)
    print 'respuesta 6'
    ret =  b.read()
    #sal = [hex(a) for a in ret]
    print ret
    print 'segunda vuelta'

    t7 = t6
    t7[-2] = t7[-2] - 1
    t7[12] = t7[12] + 1


    print 'septimo'


    b.write(t7)
    print 'res 7'
    ret =  b.read()

    print ret

    
    while True:
        #time.sleep(RETARDO)
        #print 'enviando', t7
        b.write(t7)
        t7[-2] = t7[-2] - 1
        if t7[-2] == -1:
            t7[-2] = 255
            t7[-3] = t7[-3] - 1
            

        t7[12] = t7[12] + 1
        if t7[12] == 256:
            t7[12] = 0
            t7[13] = t7[13] + 1
            t7[-2] = t7[-2] - 1


        p2 = b.read()
        
        print 'recibiendo', p2

        print "\n"



    


