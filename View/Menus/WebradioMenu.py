from PyQt5 import QtCore, QtGui, QtWidgets

from Controller.Webradio.WebradioController import WebradioController


class WebradioMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        font = QtGui.QFont()

        self.listWidget = QtWidgets.QListWidget()
        self.centralwidget = self.listWidget
        self.listWidget.setFont(font)
        self.listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.listWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setWordWrap(False)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)

        self.retranslateUi()
        self.listWidget.setCurrentRow(-1)

        self.WebradioController = WebradioController()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Zuletzt geh├Ârt"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Meine Favoriten"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Senderliste"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
