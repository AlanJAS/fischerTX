

import serial
import time

RETARDO = 1

t1 = [0x02,0x55,0x00,0x14,0x02,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x01,0x00,0x00,0x00,
      0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0xff,0xe7,0x03]
t2 = [0x02,0x55,0x00,0x18,0x02,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x02,0x00,0x01,0x00,
      0x06,0x00,0x00,0x00,0x01,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0xff,0xdb,0x03]
t3 = [0x02,0x55,0x00,0x18,0x02,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x03,0x00,0x01,0x00,
      0x07,0x00,0x00,0x00,0x01,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0xff,0xd9,0x03]
t4 = [0x0d,0x67,0x65,0x74,0x5f,0x73,0x65,0x72,0x5f,0x6e,0x75,0x6d,0x0d]

#win 9e
#linux a2

t5 = [0x02,0x55,0x00,0x48,0x02,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x01,0x00,0x00,0x00,
      0x05,0x00,0x00,0x00,0x01,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x81,0x81,0x81,0x81,0x81,0x81,0x81,0x81, 0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0xfb,0xa2,0x03]

#segunda linea del 5
#0x05,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01,

p6 = [0x02,0x55,0x00,0x44,0x02,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x02,0x00,0x02,0x00,
      0x02,0x00,0x00,0x00,0x01,0x00,0x00,0x00]



t6 = p6 + [0] * 48 + [0xff, 0xb2, 0x03]

t7 = p6 + [0] * 48 + [0xff, 0xb2, 0x03]

class Board(object):


    def __init__(self, port, baudrate=38400):
        
        self.sp = serial.Serial(port, baudrate)

        self.name = port

        time.sleep(10)
        while self.sp.inWaiting():
            r = self.sp.read()

    def write(self, data):
        r = self.sp.write(data)
        time.sleep(1)
        self.sp.flush()
        return r

    def read(self):
        #print 'reading...'
        l = []
        #s = ''
        while self.sp.inWaiting():
            r = self.sp.read()
            l.append(int(r.encode('hex'), 16))
         

        #print ':'.join('%02x' % ord(c) for c in s)
        #print  l
        
        return l

    def get_serial_number(self):
        print 'getting serial number...'
        b.write(t4)
        l = b.read()
        if len(l) > 41:
            serie = l[31:41]
            serie = ''.join(str(s) for s in serie)
            print serie
            return serie
        return ''

    def get_name(self):
        print 'getting name...'
        b.write(t4)
        l = b.read()
        name = ''
        if len(l) > 41:
            name = l[2:13]
            name = ''.join(s for s in name)
            print name
            return name
        return ''  

    def get_mac_address(self):
        print 'getting mac address...'
        b.write(t3)
        l = b.read()
        mac = ''
        if ':' in l:
            i = l.index(':')
            part = l[i-2:i+15]
            mac = ''.join(c for c in part)
            print mac
        return mac

    def update_byte(self, b, o1, o2):
        global t2, t3, t6
        
        t2[14] = b
        t3[14] = b

        t2[29] = o1
        t3[29] = o2

        t7[14] = b + 1


if __name__ == "__main__":
    print len(t1), t1
    print len(t2), t2
    print len(t3), t3
    print len(t4), t4
    print len(t5), t5
    print len(t6), t6
    
    
    b = Board('/dev/ttyACM0', 38400)

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
        
        print mn
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

    print 'hay que mandar', ret[14], hex(ret[14])

    t6[14] = ret[14]

    print 'el especial', ret[-2]

    t6[-2] = ret[-2] + 0x3b
    
    time.sleep(RETARDO) 



    print 'sexto'
    print t6
   
    b.write(t6)
    print 'respuesta 6'
    ret =  b.read()

    print ret
    print 'segunda vuelta'

    t7 = t6
    t7[-2] = t7[-2] - 1
    t7[12] = t7[12] + 1


    print 'septimo'
    print t7
    print 'res'
    b.write(t7)
    print 'respuesta 7'
    ret =  b.read()

    print ret

    t7[-2] = t7[-2] - 1
    t7[12] = t7[12] + 1

    print 'septimo'
    print t7
    print 'res'
    b.write(t7)
    print 'respuesta 7'
    ret =  b.read()

    print ret

    t7[-2] = t7[-2] - 1
    t7[12] = t7[12] + 1

    print 'septimo'
    print t7
    print 'res'
    b.write(t7)
    print 'respuesta 7'
    ret =  b.read()

    print ret
    

