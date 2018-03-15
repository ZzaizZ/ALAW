from main_form import Ui_Form
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QColor
import subprocess
import time
import parse_usb
import gzip

class MainFormSlots(Ui_Form):

	def __init__(self):
		self.q = 1
		# self.changeSelectedJournal
		# self.monitorControlUpdate
		# self.avCheck

	# метод, выводящий данные выбранного журнала
	def changeSelectedJournal(self):

		# Какой журнал выбран
		index = self.journalsTree.currentIndex()
		data = self.journalsTree.model().data(index)
		
		# очищается таблица
		self.journalText.setRowCount(0)
		self.journalText.setColumnCount(0)
		lines = ""

		# генерируем заготовку требуемой таблицы, читаем данные из нужного журнала, прописываем их:		
		# сами логи (точнее, их названия) в дерево загоняются в файле main.py
		if data != 'Системные' and data != 'Astra Linux' and data != 'Другие' and data != 'USB':
			parent = self.journalsTree.currentItem().parent().text(0)
			self.journalsTree.setHeaderLabel(parent)
			# Откуда читать журналы? Системные в /var/log, журналы Астры в /var/log/ald/
			if parent == 'Системные':
				if data[-2:] == 'gz':
					with gzip.open('/var/log/'+data, 'r') as f:
						lines = []
						for line in f.readlines():
							lines.append(line.decode('utf-8'))						
				else:						
					with open('/var/log/'+data, 'r', errors='ignore') as f:
						lines = f.readlines()
				headers = ["Дата", "Время", "Компьютер", "Событие"]
				self.journalText.setColumnCount(4)
				for i in range(0, 4):
					self.journalText.setHorizontalHeaderItem(i, QTableWidgetItem(headers[i]))
				# из-за формата журнала некоторые строки приходится объединять
				for line in lines:
					line = line.split(" ", 4)
					self.journalText.insertRow(0)
					self.journalText.setItem(0, 0, QTableWidgetItem(line[0]+" "+line[1]))
					for i in range(1, 4):
						self.journalText.setItem(0, i, QTableWidgetItem(line[i+1]))
			# заполнение логов для событий USB
			elif parent == 'USB':
				#какие заголовки столбцов будут:				
				headers = ["Дата", "Время", "Порт", "Имя", "Производитель", "ID"]
				self.journalText.setColumnCount(6)
				for i in range(0, 6):
					self.journalText.setHorizontalHeaderItem(i, QTableWidgetItem(headers[i]))
				# путь, где лежат логи. по умолчанию парсится syslog
				usb_log = '/var/log/'
				#чтение самих логов идёт через дополнительную функцию парсинга syslog
				#см. файл parse_usb.py
				logs = parse_usb.parseUSB(usb_log+data)
				for event in logs:
					if event:
						self.journalText.insertRow(0)
						for col in event[2:]:
							self.journalText.setItem(0, event.index(col)-2, QTableWidgetItem(col))
							if event[1] == 1:
								self.journalText.item(0, event.index(col)-2).setBackground(QColor(0,200,0,200))
							elif event[1] == 0:
								self.journalText.item(0, event.index(col)-2).setBackground(QColor(200,0,0,100))
			self.journalText.resizeColumnsToContents()