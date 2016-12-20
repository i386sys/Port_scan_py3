#!/usr/bin/python3
# -*- coding: utf-8 -*-

#  Auxiliary script to scan the device on the network
# over a range of 16-bit addressing ports (2 ^ 16 = 65536, beginning - '0'),
# with the result recorded in the mongodb
#  
# by Islamov Danil.
#

#import pymongo
import pymongo
import socket
from datetime import datetime
from pymongo import MongoClient

#Create data base
conn = pymongo.MongoClient('mongodb://localhost:27017/')
db = conn.port_scan

# Comment out for a fixed (non-managed) scan a specific host. Example:
host = ("10.5.2.11")
hostName = ("it-4")
# host = input('Enter host IP: ')
# hostName = input('Enter host name: ')

ports = []

for p in range(65535):
	ports.append(p)

open_port = []

# sock.settimeout(0.05) may be more or less
for port in ports:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.05)

	try:
		sock.connect((host, port))
	except:
		print('Port %s close' % port)
	else:
		open_port.append(port)
		print('Port %s open' % port)
		sock.close()

print('Open ports: ')
print (open_port)
"""
r = open ('example.txt', 'a')
r.write('### The device ' + (str(host) )+ ' with the name ' + (str(hostName)) + '\n')
r.write((datetime.today().strftime('%Y.%m.%d %H:%M')) + 
        '  The following open ports are found:  ' + (str(open_port)) + '\n')
r.write('__________________________________' + '\n')
r.close()


def full_scan(scan_ports):
	for port in ports:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.05)

		try:
			sock.connect((host, port))
		except:
			return('Port %s close' % port)
		else:
			open_port.append(port)
			return('Port %s open' % port)
			sock.close()
        
	return (open_port)
"""
db.open_port.save ({'Host':(str(host)), 'Name':(str(hostName)), 'Ports':(str(open_port)), 'Date':(datetime.today().strftime('%Y.%m.%d %H:%M'))})

