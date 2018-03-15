# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(839, 568)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mainTab = QtWidgets.QTabWidget(Form)
        self.mainTab.setObjectName("mainTab")
        self.journalsTab = QtWidgets.QWidget()
        self.journalsTab.setObjectName("journalsTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.journalsTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.journalText = QtWidgets.QTableWidget(self.journalsTab)
        self.journalText.setObjectName("journalText")
        self.journalText.setColumnCount(4)
        self.journalText.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.journalText.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.journalText.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.journalText.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.journalText.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.journalText, 0, 2, 1, 1)
        self.journalUpdateButton = QtWidgets.QPushButton(self.journalsTab)
        self.journalUpdateButton.setObjectName("journalUpdateButton")
        self.gridLayout_2.addWidget(self.journalUpdateButton, 1, 2, 1, 1)
        self.journalsTree = QtWidgets.QTreeWidget(self.journalsTab)
        self.journalsTree.setMinimumSize(QtCore.QSize(170, 0))
        self.journalsTree.setMaximumSize(QtCore.QSize(170, 16777215))
        self.journalsTree.setObjectName("journalsTree")
        item_0 = QtWidgets.QTreeWidgetItem(self.journalsTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.journalsTree)
        self.gridLayout_2.addWidget(self.journalsTree, 0, 1, 2, 1)
        self.mainTab.addTab(self.journalsTab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.mainTab.addTab(self.tab, "")
        self.gridLayout_3.addWidget(self.mainTab, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.mainTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Окно администратора"))
        item = self.journalText.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Дата"))
        item = self.journalText.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Время"))
        item = self.journalText.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Компьютер"))
        item = self.journalText.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Событие"))
        self.journalUpdateButton.setText(_translate("Form", "Обновить Журнал"))
        self.journalsTree.headerItem().setText(0, _translate("Form", "Журналы"))
        __sortingEnabled = self.journalsTree.isSortingEnabled()
        self.journalsTree.setSortingEnabled(False)
        self.journalsTree.topLevelItem(0).setText(0, _translate("Form", "Системные"))
        self.journalsTree.topLevelItem(1).setText(0, _translate("Form", "USB"))
        self.journalsTree.setSortingEnabled(__sortingEnabled)
        self.mainTab.setTabText(self.mainTab.indexOf(self.journalsTab), _translate("Form", "Журналы"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Эта программа написана с целью облегчить работу системному администратору в системе Astra Linux.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Программа тестировалась для релиза &quot;Astra Linux 1.5 Смоленск&quot;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Первая вкладка - журналы. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">На этой вкладке присутствует 3 вида журналов:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.  Системные - основные журналы, которые содержатся в любой Linux-системе. Выведены сюда для удобного просмотра важных логов</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Astra Linux - журналы, которые идут в Astra Linux. Касаются ALD и контроля пользователей. Лежат в папке /var/log/ald/*</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Другие - Журналы, которые не относятся ни к ALD ни к системным, но так же могут быть полезными (их может не быть вообще)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Вторая вкладка -  мониторинг.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Показывает общее состояние защищённости системы. Так же тут выводятся рекомендации по улучшению защищённости. В качестве критериев выступают факторы:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Наличие антивирусного ПО (Доктор Веб или Касперский)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Наличие контроля целостности файлов. Если настроен контроль целостности, выводится дата последней синхронизации.&lt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Активность системы Защищённой Среды. Учитывается, что эта система может быть включена частично (настроена только проверка ЭЦП устанавливаемых пакетов программ).</p></body></html>"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab), _translate("Form", "О программе"))

