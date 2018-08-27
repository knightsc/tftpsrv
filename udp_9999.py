# Scans a network for vulnerable D-Link DPH-128MS phones

from socket import *
import sys

ip = '192.168.1.'
port = 9999

data = '?'

for i in range(1,256):
  address = (ip+str(i),port)
  #print address
  
  try:
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.settimeout(0.5)
    UDPSock.sendto(data, address)
    
    response,addr = UDPSock.recvfrom(1024)
    if 'DPH-128MS' in response and '01.15.10' in response:
      print ip+str(i)    
  except:
    pass
  finally:
    UDPSock.close()