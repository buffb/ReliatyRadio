from datetime import datetime
import vlc
from PyQt5 import QtCore, QtGui, QtWidgets

from Model.DatabaseController import DatabaseController, db_session, Webradio
from Controller.PlayerGpioController import PlayerGpioController
from View.Menus.StationListPicker import StationListPicker
from Util import QIconHelper

import os

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


class ReliatyPlayer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.db = DatabaseController.get_instance()
        self.gpio = PlayerGpioController()
        self.gpio.controller.switch_callback = self.play_pause

        self.v = vlc.Instance("--aout=alsa")
        self.player = self.v.media_player_new()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.setup_ui()

        # Start with last played station
        with db_session:
            station = self.db.get_stations_by_last_played()[0]
            self.change_station(station)
        self.setup_buttons()

    def setup_ui(self):
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.toolButton_home = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_home.setGeometry(QtCore.QRect(10, 10, 81, 71))
        self.toolButton_home.setStyleSheet("QToolButton{\n"
                                           "border: none ;\n"
                                           "background: transparent ;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:pressed{\n"
                                           "background-color : rgb(255, 255, 255)\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_home.setIcon(icon)
        self.toolButton_home.setIconSize(QtCore.QSize(50, 50))
        self.toolButton_home.setObjectName("toolButton_home")

        # self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        # self.horizontalSlider.setGeometry(QtCore.QRect(130, 400, 831, 21))
        # self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        # self.horizontalSlider.setObjectName("horizontalSlider")

        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(100, 10, 221, 51))
        self.label_logo.setStyleSheet("image: url(:/icons/logo.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")

        self.playercontrolbar = QtWidgets.QWidget(self.centralwidget)
        self.playercontrolbar.setGeometry(QtCore.QRect(0, 400, 1021, 141))
        self.playercontrolbar.setObjectName("playercontrolbar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.playercontrolbar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toolButton_play = QtWidgets.QToolButton(self.playercontrolbar)
        self.toolButton_play.setStyleSheet("QToolButton{\n"
                                           "border: none ;\n"
                                           "background: transparent ;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:pressed{\n"
                                           "background-color : rgb(255, 255, 255)\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon1 = QtGui.QIcon()

        icon1.addPixmap(QtGui.QPixmap(":icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.toolButton_play.setIcon(icon1)
        self.toolButton_play.setCheckable(True)
        self.toolButton_play.setIconSize(QtCore.QSize(200, 200))
        self.toolButton_play.setObjectName("toolButton_play")
        self.horizontalLayout.addWidget(self.toolButton_play)

        self.toolButton_mute = QtWidgets.QToolButton(self.playercontrolbar)
        self.toolButton_mute.setStyleSheet("QToolButton{\n"
                                           "border: none ;\n"
                                           "background: transparent ;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:pressed{\n"
                                           "background-color : rgb(255, 255, 255)\n"
                                           "}\n"
                                           "\n"
                                           "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":icons/mute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":icons/unmute.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.toolButton_mute.setCheckable(True)
        self.toolButton_mute.setIcon(icon2)
        self.toolButton_mute.setIconSize(QtCore.QSize(200, 200))
        self.toolButton_mute.setObjectName("toolButton_mute")
        self.horizontalLayout.addWidget(self.toolButton_mute)
        self.toolButton_senderwahl = QtWidgets.QToolButton(self.playercontrolbar)
        self.toolButton_senderwahl.setStyleSheet("QToolButton{\n"
                                                 "border: none ;\n"
                                                 "background: transparent ;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QToolButton:pressed{\n"
                                                 "background-color : rgb(255, 255, 255)\n"
                                                 "}\n"
                                                 "\n"
                                                 "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":icons/senderauswahlX.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_senderwahl.setIcon(icon3)
        self.toolButton_senderwahl.setIconSize(QtCore.QSize(200, 200))
        self.toolButton_senderwahl.setObjectName("toolButton_senderwahl")
        self.horizontalLayout.addWidget(self.toolButton_senderwahl)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 130, 1011, 231))
        self.widget.setObjectName("widget")
        self.station_4 = QtWidgets.QToolButton(self.widget)

        self.station_4.setGeometry(QtCore.QRect(180, 30, 141, 161))
        self.station_4.setStyleSheet("QToolButton{\n"
                                     "border: none ;\n"
                                     "background: transparent ;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:pressed{\n"
                                     "background-color : rgb(255, 255, 255)\n"
                                     "}\n"
                                     "\n"
                                     "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":icons/fav3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.station_4.setIcon(icon4)
        self.station_4.setIconSize(QtCore.QSize(300, 300))
        self.station_4.setObjectName("station_4")
        self.station_2 = QtWidgets.QToolButton(self.widget)

        self.station_2.setGeometry(QtCore.QRect(280, 30, 171, 161))
        self.station_2.setStyleSheet("QToolButton{\n"
                                     "border: none ;\n"
                                     "background: transparent ;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:pressed{\n"
                                     "background-color : rgb(255, 255, 255)\n"
                                     "}\n"
                                     "\n"
                                     "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":icons/fav1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.station_2.setIcon(icon5)
        self.station_2.setIconSize(QtCore.QSize(300, 300))
        self.station_2.setObjectName("station_2")
        self.station_1 = QtWidgets.QToolButton(self.widget)

        self.station_1.setGeometry(QtCore.QRect(410, 20, 201, 181))
        self.station_1.setStyleSheet("QToolButton{\n"
                                     "border: none ;\n"
                                     "background: transparent ;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:pressed{\n"
                                     "background-color : rgb(255, 255, 255)\n"
                                     "}\n"
                                     "\n"
                                     "")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":icons/c175.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.station_1.setIcon(icon6)
        self.station_1.setIconSize(QtCore.QSize(300, 300))
        self.station_1.setObjectName("station_1")
        self.station_3 = QtWidgets.QToolButton(self.widget)

        self.station_3.setGeometry(QtCore.QRect(580, 30, 171, 161))
        self.station_3.setStyleSheet("QToolButton{\n"
                                     "border: none ;\n"
                                     "background: transparent ;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:pressed{\n"
                                     "background-color : rgb(255, 255, 255)\n"
                                     "}\n"
                                     "\n"
                                     "")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":icons/fav2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.station_3.setIcon(icon7)
        self.station_3.setIconSize(QtCore.QSize(300, 300))
        self.station_3.setObjectName("station_3")
        self.station_5 = QtWidgets.QToolButton(self.widget)

        self.station_5.setGeometry(QtCore.QRect(730, 30, 141, 161))
        self.station_5.setStyleSheet("QToolButton{\n"
                                     "border: none ;\n"
                                     "background: transparent ;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:pressed{\n"
                                     "background-color : rgb(255, 255, 255)\n"
                                     "}\n"
                                     "\n"
                                     "")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":icons/fav4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.station_5.setIcon(icon8)
        self.station_5.setIconSize(QtCore.QSize(300, 300))
        self.station_5.setObjectName("station_5")
        self.station_5.raise_()
        self.station_4.raise_()
        self.station_2.raise_()
        self.station_3.raise_()
        self.station_1.raise_()

    def populate_wigets(self):
        with db_session:
            stations = list(self.db.get_stations_by_last_played())
            widgetlist = [self.station_2, self.station_3, self.station_4, self.station_5]
            for widget in widgetlist:
                unpopulated = True
                while unpopulated:
                    if len(stations) <= 0:
                        break
                    station = stations.pop(0)
                    if self.station is not None and station.name == self.station.name: continue
                    iconable, icon = QIconHelper.qicon_from_binary_image(station.icon, greyscale=True)
                    if not iconable: continue

                    widget.setIcon(icon)
                    station.load()
                    widget.setProperty("station", station)
                    widget.disconnect()  # prohibit multiple connections
                    widget.clicked.connect(self.on_change_station)
                    unpopulated = False
            return

    def setup_player(self):
        if self.station is not None:
            self.player.set_mrl(self.station.url)
            self.play_pause()

    def setup_buttons(self):
        self.toolButton_play.clicked.connect(self.play_pause)
        self.toolButton_mute.clicked.connect(self.mute_unmute)
        self.toolButton_home.clicked.connect(self.go_home)
        self.toolButton_senderwahl.clicked.connect(self.open_station_picker)

    def open_station_picker(self):
        self.nativeParentWidget().add_and_show_widget(StationListPicker(player=self))

    def go_home(self):
        self.player.release()
        self.gpio.stop()
        self.nativeParentWidget().show_main_menu()

    def play_pause(self):
        if self.player.is_playing() == 0:
            self.player.play()
            self.toolButton_play.setChecked(True)
        else:
            self.player.pause()
            self.toolButton_play.setChecked(False)

    def mute_unmute(self):
        self.player.audio_toggle_mute()

    def on_change_station(self):
        station = self.sender().property("station")
        self.change_station(station=station)

    def change_station(self, station=None):
        self.station = station
        self.player.stop()
        with db_session:
            station = Webradio.get(name=station.name)
            station.clickcount = +1
            station.last_played = datetime.utcnow()
            station.load()
        _, icon = QIconHelper.qicon_from_binary_image(station.icon)
        self.station_1.setIcon(icon)
        self.station_1.setProperty("station", station)
        self.populate_wigets()
        self.setup_player()
