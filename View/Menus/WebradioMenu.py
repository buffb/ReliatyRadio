from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QStackedLayout

import WebradioPlayer
from Model.DatabaseController import DatabaseController, db_session
from View.CallableListItem import CallableListItem
from View.Menus import MainMenu


class WebradioMenu(QtWidgets.QWidget):
    def __init__(self,main_menu, parent=None):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.main_menu = main_menu
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setFont(font)
        self.listWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.listWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")

        self.listWidget.clicked.connect(self.handle_item)
        self.listWidget.setCurrentRow(-1)

        self.show_menu()
        self.retranslateUi()
        self.db = DatabaseController.get_instance()

    def handle_item(self):
        item = self.listWidget.currentItem()
        item.item()

    def show_menu(self):
        items= [
            CallableListItem(name="Zuletzt gespielt",item=self.show_lastPlayed),
            CallableListItem(name="Genres",item=self.show_genres),
            CallableListItem(name="Alle Sender",item=self.show_stations),
            CallableListItem(name="Zurück",item=self.main_menu.show)
            ]
        self.clearAndSetMenu(items)

    def show_lastPlayed(self):
        pass

    def show_stations(self):
        with db_session:
            items = self.db.get_radio_stations_by_popularity()
            self.clearAndSetMenu(items)

    def show_genres(self):
        with db_session:
            items = self.db.get_genres_by_count()
            itemlist= [CallableListItem(name=g.name, item=self.show_stations_by_genre, params=[g.name])for g in items]
            self.clearAndSetMenu(itemlist)

    def show_stations_by_genre(self):
        item = self.listWidget.currentItem()
        with db_session:
            genre = item.params[0]
            stations = self.db.get_radio_stations_by_genre(genre)
            items = [CallableListItem(name=s.name, item=self.show_player, params=s) for s in stations]
            self.clearAndSetMenu(items)

    def show_player(self):
        item = self.listWidget.currentItem()
        self.main_menu.show_player(item.params)

    def clearAndSetMenu(self, items):
        self.listWidget.clear()
        for item in items:
            self.listWidget.addItem(item)
        self.listWidget.selectedIndexes().clear()

    def retranslateUi(self):
        pass
        # _translate = QtCore.QCoreApplication.translate
        # __sortingEnabled = self.listWidget.isSortingEnabled()
        # self.listWidget.setSortingEnabled(False)
        # item = self.listWidget.item(0)
        # item.setText(_translate("MainWindow", "Zuletzt gehört"))
        # item = self.listWidget.item(1)
        # item.setText(_translate("MainWindow", "Alle Sender"))
        # item = self.listWidget.item(2)
        # item.setText(_translate("MainWindow", "Genres"))
        # self.listWidget.setSortingEnabled(__sortingEnabled)
