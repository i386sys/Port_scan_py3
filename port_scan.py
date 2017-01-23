#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Простой скрипт для сканирования устройств в сети 
# с учетом 16-битной адресации (2^16 = 65536, начало 0)
# с записью результата в базу данных MongoDB

# Импортируем необходимые модули
import pymongo
import socket
import time
from datetime import datetime
from pymongo import MongoClient

# Создаем базу данных
# Адрес по умолчанию localhost:27017
connection = pymongo.MongoClient()
db = connection.port_scan

# Определяем устройство для сканирования
# Для статичного ввода используйте:
# host = ("192.168.1.1")
# hostName = ("Example")
# city = ("Example")

print('Здравствуйте! Введите данные устройства,' + '\n' +
	  'которое необходимо проверить на открытые порты.' + '\n')

try:
	host = input('IP адрес: ')
	hostName = input('Имя: ')
	city = input('Город: ')

# Разбираем строку host для проверки
# корректности введенного IP адреса
	host.split('.')
	hostIP = host.split('.')
	hostIP = [int(item) for item in hostIP]

# В случае некорректного IP, вызывается
# исключение с приглашением ввести IP снова
except:
	print('IP адрес должен содержать только цифры и точки')
	host = input('IP: ')
	host.split('.')
	hostIP = host.split('.')
	hostIP = [int(item) for item in hostIP]

try:
	if len(hostIP) == len([number for number in hostIP if number >= 0]):
		print('Идет сканирование портов...' + '\n')

except ValueError:
	print('IP введен не верно.')

# Старт таймера
start_t = time.time()

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
		pass
	else:
		open_port.append(port)
		sock.close()

# Остановка таймера, подсчет времени
stop_t = time.time()
done_time = stop_t - start_t

# Вывод открытых портов в консоль
print('Открытые порты ' + hostName + ': ')
print(open_port)

# Запись в базу данных IP адреса, имени устройства, открытых портов и даты сканирования
db.open_port.save ({'Host':(str(host)), 'Name':(str(hostName)), 'Ports':(str(open_port)), 
	'Date':(datetime.today().strftime('%Y.%m.%d %H:%M')), 'City':(str(city))})

print('\n' + 'Время на выполнение (сек): ')
print(done_time)
