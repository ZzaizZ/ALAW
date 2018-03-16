from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
import gzip

class LogString():
	
	def __init__(self, log_name = 'syslog'):
		self.log_name = log_name

	def __prepare_string(self, origin_string):
		splitted_string = origin_string.split()
		log_string = {"Date": "", "Time": "", "Source": "", "ProcessName": "", "Event": ""}
		log_string['Month'] = splitted_string[0] + " " + splitted_string[1]
		log_string['Time'] = splitted_string[2]
		log_string['Source'] = splitted_string[3]
		log_string['ProcessName'] = splitted_string[4][:-1]
		log_string['Event'] = splitted_string[5]
		return log_string

	def get_log_str(self):
		return self.__prepare_string()

class SystemLog():
	'''
		Класс системного лога
		(тестировалось на syslog, kern.log, auth.log)

		суть класса - подцеплять указанный лог, читать его и обрабатывать построчно

		_read_log() - читает указанный лог (путь до лога должен быть полный) и парсит лог построчно,
					разбивая его на стандартные для системных логов столбцы:
					Дата, Время, ИмяПК, Процесс, Событие <- структура получаемой строки лога
					Все строки записываются в список log_strings[]

		print_log(tree) - выводит прочитанный лог в таблицу QTableWidget, объект которого и передаётся
					этому методу в качестве аргумента. Он сам создаёт нужное количество столбцов, задаёт
					им имена и пишет лог построчно из списка log_strings[] в QTableWidget
	'''
	
	def __init__(self, log_name):
		self.log_name = log_name
		self.log_strings = []

	def _read_log(self):
		if self.log_name[-2:] == 'gz':
			with gzip.open(self.log_name, 'r') as f:
				lines = []
				for line in f.readlines():
					lines.append(line.decode('utf-8')) # !!!BUG баг с не-юникодовскими символами 0x96						
		else:						
			with open(self.log_name, 'r') as f:
				lines = f.readlines()
		for log_string in lines:
			splitted_string = log_string.split() # !!!TIP возможно, стоит использовать регулярки для более грамотного парсинга строки
			log_string = {"Date": "", "Time": "", "Source": "", "ProcessName": "", "Event": ""}
			log_string['Date'] = splitted_string[0] + " " + splitted_string[1]
			log_string['Time'] = splitted_string[2]
			log_string['Source'] = splitted_string[3]
			log_string['ProcessName'] = splitted_string[4][:-1]
			log_string['Event'] = "".join(splitted_string[5:])
			self.log_strings.append(log_string)
	
	def print_log(self, tree):
		self._read_log()
		headers = ["Дата", "Время", "Компьютер", "Процесс","Событие"]
		headrers_count = len(headers)

		if headrers_count != len(self.log_strings[0]):
			print(headrers_count, len(self.log_strings[0]))
			print('Несовпадение количества столбцов и частей строк')
			return -1

		tree.setColumnCount(headrers_count)
		for i in range(len(self.log_strings[0])):
			tree.setHorizontalHeaderItem(i, QTableWidgetItem(headers[i]))
		for log_line in self.log_strings:
			tree.insertRow(0)
			tree.setItem(0, 0, QTableWidgetItem(log_line['Date']))
			tree.setItem(0, 1, QTableWidgetItem(log_line['Time']))
			tree.setItem(0, 2, QTableWidgetItem(log_line['Source']))
			tree.setItem(0, 3, QTableWidgetItem(log_line['ProcessName']))
			tree.setItem(0, 4, QTableWidgetItem(log_line['Event']))
		return 0
