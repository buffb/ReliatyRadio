#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStackedLayout,QMainWindow,QWidget

from View.Menus.MainMenu import *


class ReliatyRadio(QMainWindow):
    layout = None

    back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_layout()

        # Generic UI Settings
        self.resize(1024, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.show_main_menu()

    def init_layout(self):
        self.layout = QStackedLayout()
        self.setCentralWidget(QWidget())
        self.centralWidget().setSizePolicy(self.sizePolicy())
        self.centralWidget().resize(1024, 600)
        self.centralWidget().setLayout(self.layout)

    def add_and_show_widget(self, widget):
        self.layout.addWidget(widget)
        self.layout.setCurrentWidget(widget)

    def go_back(self):
        count = self.layout.count()
        self.layout.setCurrentIndex(count - 2)
        self.layout.takeAt(count - 1)

    def show_main_menu(self):
        self.clearLayout()
        self.add_and_show_widget(MainMenu())

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ReliatyRadio()
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
