#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Простой скрипт для сканирования устройств в сети 
# с учетом 16 битной адресации (2^16 = 65536, начало 0)
# с зхаписью результата в базу данных MongoDB
#
# Исламов Данил

# Импортируем необходимые модули
import pymongo
import socket
from datetime import datetime
from pymongo import MongoClient

#Создаем базу данных
conn = pymongo.MongoClient()
db = conn.port_scan

# Определяем устройство для сканирования
# Для динамического ввода используйте
# host = input('IP устройства: ')
# hostName = input('Имя устройства: ')
host = ("10.5.2.11")
hostName = ("it-4")

# Определяем список всех портов
ports = []

for p in range(65535):
	ports.append(p)

# Определяем список открытых портов
open_port = []

# Сканируем все порты с задержкой 0.05 
# можно увеличить или уменьшить при необходимости
# Открытые порты добавляются в конец списка открытых портов
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

# Вывод открытых портов в консоль
print('Open ports: ')
print (open_port)

# Запись в базу данных IP адреса, имени устройства, открытых портов и даты сканирования
db.open_port.save ({'Host':(str(host)), 'Name':(str(hostName)), 'Ports':(str(open_port)), 'Date':(datetime.today().strftime('%Y.%m.%d %H:%M'))})

