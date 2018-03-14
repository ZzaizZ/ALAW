#!/usr/bin/python3

import sys
import re
import gzip
# Импортируем минимальный набор виджетов
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
# Импортируем созданный нами класс со слотами
import main_slots
from os import listdir

# Создаём ещё один класс, наследуясь от класса со слотами
class MainForm(main_slots.MainFormSlots):

    # При инициализации класса нам необходимо выпонить некоторые операции
    def __init__(self, form):
        # Сконфигурировать интерфейс методом из базового класса Ui_Form
        self.setupUi(form)
        # далее, донастройка интерфейсов
        self.journalText.horizontalHeader().setStretchLastSection(True)
        # чтение ВСЕХ имеющихся логов у астры (в основном - ald)
        logPath = "/var/log/"
        try:
            ald_logs = [f for f in listdir(logPath+"ald/")]
            kern_logs = [f for f in listdir(logPath) if re.search(r"kern\.log.?[0-9]*", f)]
            for i in range(0, len(ald_logs)):
            	item = QtWidgets.QTreeWidgetItem()
            	item.setText(0, ald_logs[i])
            	self.journalsTree.topLevelItem(1).addChild(item)
            for i in range(0, len(kern_logs)):
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, kern_logs[i])
                self.journalsTree.topLevelItem(0).addChild(item)
        except IOError as e:
            print('Ошибка при чтении логов астры.\nПроверьте путь \/var\/log\/ald\/')
            pass
            #логгирование
        # чтение  дополнительных логов
        try:
            file = open('~/.ald/')
        except IOError as e:
            pass
            #ЛОГГИРОВАНИЕ
        else:
            ald_logs = [f for f in listdir("~/.ald/")]
            for i in range(0, len(ald_logs)):
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, ald_logs[i])
                self.journalsTree.topLevelItem(3).addChild(item)
        # чтение логов подключения USB
        try:
            # чтение конкретных файлов по заданному паттернудля usb
            usb_logs_path = "/var/log"
            usb_logs = [f for f in listdir(usb_logs_path) if re.search(r"syslog.?[0-9]*", f)]
            print(usb_logs)
            for i in range(0,len(usb_logs)):
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, usb_logs[i])
                # item.setText(0, "usb event " + str(i))
                self.journalsTree.topLevelItem(2).addChild(item)
        except IOError as e:
            print("Не удалось открыть лог USB: %s" % (e))
            pass
            
        # Подключить созданные нами слоты к виджетам
        self.connect_slots()

    # Подключаем слоты к виджетам
    def connect_slots(self):
        self.journalsTree.selectionModel().selectionChanged.connect(self.changeSelectedJournal)
        self.journalUpdateButton.clicked.connect(self.changeSelectedJournal)
        return None

if __name__ == '__main__':
    # Создаём экземпляр приложения
    app = QApplication(sys.argv)
    # Создаём базовое окно, в котором будет отображаться наш UI
    window = QWidget()
    # Создаём экземпляр нашего UI
    ui = MainForm(window)
    # Отображаем окно
    window.show()
    # Обрабатываем нажатие на кнопку окна "Закрыть"
    sys.exit(app.exec_())