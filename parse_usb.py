#!/usr/bin/python3
import re
import gzip

#в этом файле содержится всё что нужно для парсинга событий USB в syslog
#класс USB просто для удобства, что бы можно было вытаскивать данные по устройству
class USBDevice:
	def __init__(self, product=None, vendor=None, serN=None):
		self.product = product
		self.vendor = vendor
		self.serN = serN

	def __str__(self):
		return str("USB Device: %s; vendor: %s; serial: %s;" % (self.product, self.vendor, self.serN))

	def getProduct(self):
		return str(self.product)

	def getVendor(self):
		return str(self.vendor)

	def getSerN(self):
		return str(self.serN)

	def setProduct(self, data):
		self.product = data

	def setVendor(self, data):
		self.vendor = data

	def setSerN(self, data):
		self.serN = data

# основная функция парсинга
# читает стандартный syslog
def parseUSB(file):
	if file[-2:] == 'gz':
		with gzip.open(file, 'r') as f:
			lines = f.readlines()
	else:						
		with open(file, 'r') as f:
			lines = f.readlines()
	# стандартный шаблон для regexp
	usb_pat = r'usb [0-9]-[0-9]:'
	# переменные для хранения результатов
	result = []
	tmp_result = []
	devices = []
	device = USBDevice()

	# построчное чтение syslog
	for line in lines:
		if file[-2:] == 'gz':
			line = line.decode('utf-8')
		# поиск строк с usb событиями
		usbs = re.search(usb_pat, line)
		if usbs:
			# Структура формируемого списка:
			# номер устройства, статус (1 - подкл, 0 - выкл), дата, время, порт, имя, производитель, ID
			# Проверяем устройства из списка, отключены ли они
			usb_discon_pat = r'usb [0-9]-[0-9]: USB disconnect, device number [0-9]+'
			st = re.search(usb_discon_pat, line)
			if st:
				tmp_line = line.split()
				number = tmp_line[-1]
				for e in result:
					if e and e != '' and int(e[0]) == int(number)-1 and e[1] == 1:
						tmp_result = e[:]
						tmp_result[1] = 0
						tmp_result[2] = " ".join(tmp_line[0:2])
						tmp_result[3] = tmp_line[2]
						break
				result.append(tmp_result)
				tmp_result=[]
				continue
			# Ищем первое сообщение о новом USB устройстве.
			# Оттуда помимо времени нужен device number
			# используя это значение можно определить, когда это устройство было подключено
			usb_first_pat = r'new (high)|(full)-speed USB device number [0-9]+'
			st = re.search(usb_first_pat, line)
			if st:
				if tmp_result and tmp_result[1] != 0:
					result.append(tmp_result)
				tmp_result = []
				devices.append(device)
				device = USBDevice()
				tmp_line = line.split()
				if tmp_line[5] == '[':
					tmp_line.remove('[')
				tmp_result.append(int(tmp_line[13])) # 13/14 было
				tmp_result.append(1)
				tmp_result.append(" ".join(tmp_line[0:2]))
				tmp_result.append(tmp_line[2])
				tmp_result.append(tmp_line[7][0:-1]) # 7/8

			# ниже идут три условия парсинга производителя, продукта и ID
			usb_prod_pat = r'Product: [a-zA-Z0-9 ]'
			st = re.search(usb_prod_pat, line)
			if st:
				tmp_line = line.split()
				device.setProduct((" ".join(tmp_line[10:]))[0:])
				tmp_result.append(device.getProduct())
			
			usb_vend_pat = r'Manufacturer: [a-zA-Z0-9 ]'
			st = re.search(usb_vend_pat, line)
			if st:
				tmp_line = line.split()
				device.setVendor((" ".join(tmp_line[10:]))[0:])
				tmp_result.append(device.getVendor())
			
			usb_serN_pat = r'SerialNumber: [a-zA-Z0-9 ]'
			st = re.search(usb_serN_pat, line)
			if st:
				tmp_line = line.split()
				device.setSerN((" ".join(tmp_line[10:]))[0:])
				tmp_result.append(device.getSerN())
	return(result)