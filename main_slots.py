from main_form import Ui_Form
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QColor
import subprocess
import time
import parse_usb
import gzip
from alLogs import SystemLog

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
		# сами логи (точнее, их названия) в дерево загоняются автоматически в main.py
		if data != 'Системные' and data != 'Astra Linux' and data != 'Другие' and data != 'USB':
			parent = self.journalsTree.currentItem().parent().text(0)
			self.journalsTree.setHeaderLabel(parent)
			# Откуда читать журналы? Системные в /var/log
			log_containers = ['kern', 'syslog', 'auth']
			if parent in log_containers:
				log_file = SystemLog('/var/log/'+data)
				success = log_file.print_log(self.journalText)
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
						for col in headers:
							if col in event.keys():
								self.journalText.setItem(0, headers.index(col), QTableWidgetItem(event[col]))
						if event['status'] == 'disconnected':
							for cell_index in range(3):
								self.journalText.item(0, cell_index).setBackground(QColor(200,0,0,100))
						elif event['status'] == 'connected':
							for cell_index in range(len(event.keys())-2):
								self.journalText.item(0, cell_index).setBackground(QColor(0,200,0,100))
			self.journalText.resizeColumnsToContents()