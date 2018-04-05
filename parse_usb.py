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
	
	# переменные для хранения результатов
	result = []
	device = USBDevice()

	# стандартный шаблон для regexp
	usb_pat = r'usb [0-9]-[0-9]:'
	# построчное чтение syslog
	for line in lines:
		if file[-2:] == 'gz':
			line = line.decode('utf-8')
		# поиск строк с usb событиями
		usbs = re.search(usb_pat, line)
		tmp_result = {}
		#если в строке лога идёт событие, связанное с usb-портом
		if usbs:
			# Структура формируемого списка:
			# статус, номер устройства, дата, время, порт, имя, производитель, ID
			new_usb_pat = r'^([A-Z][a-z]{2}\s+[1-9]{1,2}).+(([0-9]{2}:){2}[0-9]{2}).*usb ([1-9]-[1-9]): new ((high)|(full))-speed USB device number ([0-9]+)'
			dis_usb_pat = r'^([A-Z][a-z]{2}\s+[1-9]{1,2}).+(([0-9]{2}:){2}[0-9]{2}).*usb ([1-9]-[1-9]): USB disconnect, device number ([0-9]+)'
			st_new = re.search(new_usb_pat, line)
			st_dis = re.search(dis_usb_pat, line)
			if st_new:				
				tmp_result['status'] = 'connected'
				tmp_result['dev_number'] = st_new.group(8)
				tmp_result['Дата'] = st_new.group(1)
				tmp_result['Время'] = st_new.group(2)
				tmp_result['Порт'] = st_new.group(4)
			elif st_dis:
				tmp_result['status'] = 'disconnected'
				tmp_result['dev_number'] = st_dis.group(5)
				tmp_result['Порт'] = st_dis.group(4)
				tmp_result['Дата'] = st_dis.group(1)
				tmp_result['Время'] = st_dis.group(2)

			if tmp_result:
				result.append(tmp_result)
			tmp_result = {}
		# ниже идут три условия парсинга производителя, продукта и ID
		if len(result) > 0:
			usb_prod_pat = r'Product: ([a-zA-Z0-9 ]+)\n?'
			st = re.search(usb_prod_pat, line)
			if st:
				device.setProduct(st.group(1))
				result[-1]['Имя'] = device.getProduct()
			
			usb_vend_pat = r'Manufacturer: ([a-zA-Z0-9 ]+)\n?'
			st = re.search(usb_vend_pat, line)
			if st:
				device.setVendor(st.group(1))
				result[-1]['Производитель'] = device.getVendor()
			
			usb_serN_pat = r'SerialNumber: ([a-zA-Z0-9 _-]+)\n?'
			st = re.search(usb_serN_pat, line)
			if st:
				device.setSerN(st.group(1))
				result[-1]['ID'] = device.getSerN()
	return(result)