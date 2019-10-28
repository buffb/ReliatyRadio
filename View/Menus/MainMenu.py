# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStackedLayout, QMainWindow

from View.Menus.SettingsMenu import SettingsMenu
from View.Menus.WebradioMenu import WebradioMenu


class MainMenu(QMainWindow):

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("main_window", "Reliaty Radio"))
        self.listWidget.setSortingEnabled(False)

        item = self.listWidget.item(0)
        item.setText(_translate("main_window", "Webradio"))
        item = self.listWidget.item(1)
        item.setText(_translate("main_window", "Einstellungen"))
        item = self.listWidget.item(2)
        item.setText(_translate("main_window", "Exit"))

    def create_submenu(self, index):
        item = index.row()
        print(item)
        if item == 0:  self.layout.addWidget(WebradioMenu(self))
        if item == 1: self.layout.addWidget(SettingsMenu(self))
        if item == 2: sys.exit(1)

        self.layout.setCurrentIndex(self.layout.count() - 1)

    def show(self):
        self.layout.setCurrentWidget(self.listWidget)

    def __init__(self):
        super().__init__()
        # This holds the layouts for all subsequent menu views
        self.centralwidget = QtWidgets.QWidget()
        self.layout = QStackedLayout()
        self.centralwidget.setLayout(self.layout)
        self.setCentralWidget(self.centralwidget)
        # Create initial layout of the main menu
        self.setObjectName("MainMenu")
        self.resize(1024, 768)

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)

        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget()
        self.layout.addWidget(self.listWidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 1024, 768))

        self.listWidget.setFont(font)
        # self.listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listWidget.setLineWidth(1)
        self.listWidget.setCurrentRow(-1)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setAlternatingRowColors(False)
        self.listWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setWordWrap(False)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem(self.listWidget)
        item = QtWidgets.QListWidgetItem(self.listWidget)
        item = QtWidgets.QListWidgetItem(self.listWidget)
        self.listWidget.clicked.connect(self.create_submenu)

        self.retranslate_ui()

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())

        self.listWidget.setSizePolicy(sizePolicy)
        self.centralwidget.setSizePolicy(sizePolicy)


