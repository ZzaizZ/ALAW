#!/usr/bin/python3

#coding:windows-1252

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
        self.journalText.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.journalText.setSortingEnabled(True)
        # чтение логов системы
        logPath = "/var/log/"
        try:
            # Составление списков журналов и их вывод в дерево навигации
            kern_logs = [f for f in listdir(logPath) if re.search(r"kern\.log.?[0-9]*", f)]
            sys_logs = [f for f in listdir(logPath) if re.search(r'syslog\.?[0-9]*', f)]
            auth_logs = [f for f in listdir(logPath) if re.search(r'auth\.log.?[0-9]*', f)]
            topLevelItem = self.journalsTree.topLevelItem(0)
            kern_root = QtWidgets.QTreeWidgetItem(topLevelItem)
            self.journalsTree.addTopLevelItem(topLevelItem)
            kern_root.setText(0, 'kern')
            for kern_log in kern_logs:
                item = QtWidgets.QTreeWidgetItem(kern_root)
                self.journalsTree.addTopLevelItem(item)
                item.setText(0, kern_log)
                item.setText(1, 'log')
            sys_root = QtWidgets.QTreeWidgetItem(topLevelItem)
            self.journalsTree.addTopLevelItem(topLevelItem)
            sys_root.setText(0, 'syslog')
            for sys_log in sys_logs:
                item = QtWidgets.QTreeWidgetItem(sys_root)
                self.journalsTree.addTopLevelItem(item)
                item.setText(0, sys_log)
            auth_root = QtWidgets.QTreeWidgetItem(topLevelItem)
            self.journalsTree.addTopLevelItem(topLevelItem)
            auth_root.setText(0, 'auth')
            for auth_log in auth_logs:
                item = QtWidgets.QTreeWidgetItem(auth_root)
                self.journalsTree.addTopLevelItem(item)
                item.setText(0, auth_log)
        except IOError as e:
            print('Ошибка при чтении логов системы.\nПроверьте путь \/var\/log\/ и права доступа до файла.')
            pass
            #логгирование
        # чтение логов подключения USB
        try:
            # чтение конкретных файлов по заданному паттернудля usb
            usb_logs_path = "/var/log"
            usb_logs = [f for f in listdir(usb_logs_path) if re.search(r"syslog.?[0-9]*", f)]
            topLevelItem = self.journalsTree.topLevelItem(0)
            usb_root = QtWidgets.QTreeWidgetItem(topLevelItem)
            for i in range(0,len(usb_logs)):

                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, usb_logs[i])
                self.journalsTree.topLevelItem(1).addChild(item)
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
    # Отображаем окн
    window.show()
    # Обрабатываем нажатие на кнопку окна "Закрыть"
    sys.exit(app.exec_())