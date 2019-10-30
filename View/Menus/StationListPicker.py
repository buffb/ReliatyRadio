from enum import Enum

from PyQt5 import QtCore, QtGui, QtWidgets

from Model.DatabaseController import DatabaseController, db_session, desc, Webradio
from Util import QIconHelper


class Sorting(Enum):
    by_popularity = 1
    by_name = 2


class StationListPicker(QtWidgets.QWidget):
    def __init__(self,player=None):
        super().__init__()
        self.db = DatabaseController.get_instance()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setup_ui()

        self.page= 1
        self.perpage= 15

        self.player = player

        self.sorting = None
        self.genre = None

        self.populate_boxes()
        self.populate_grid()

    def populate_boxes(self):
        with db_session:
            # Genres
            self.box_genre.addItem("Alle Genres")
            genres = self.db.get_genres_by_count()
            for genre in genres[0:10:1]:
                self.box_genre.addItem(genre.name, genre)

            self.box_genre.currentIndexChanged.connect(self.filter_genre)

            # Sorting
            self.box_sort.addItem("nach Beliebtheit", Sorting.by_popularity)
            self.box_sort.addItem("nach Name", Sorting.by_name)

            self.box_sort.currentIndexChanged.connect(self.set_sorting)

            self.btn_next.clicked.connect(self.next_page)
            self.btn_prev.clicked.connect(self.prev_page)


    def next_page(self):
        self.page+=1
        self.populate_grid()

    def prev_page(self):
        self.page-=1
        self.populate_grid()

    def populate_grid(self):
        with db_session:
            stations = self.db.get_radio_stations()
            if self.genre is not None:
                stations = stations.filter(lambda s: self.genre in s.genres)

            if self.sorting is None or self.sorting == Sorting.by_popularity:
                stations = stations.order_by(desc(Webradio.popularity))

            if self.sorting == Sorting.by_name:
                stations = stations.order_by(desc(Webradio.name))

            stationlist = list(stations.page(self.page,self.perpage))

            for row in range(0, 3, 1):
                for col in range(1, 6, 1):
                    widget = self.gridLayout.itemAtPosition(row, col).widget()
                    success = False
                    while not success:
                        if len(stationlist) > 0:
                            station = stationlist.pop(0)

                            iconable, icon = QIconHelper.qicon_from_binary_image(station.icon)
                            if not iconable: continue
                            widget.setIcon(icon)
                            station.load()
                            widget.setProperty("station", station)
                            widget.clicked.connect(self.play_station)
                            success = True
                        else:
                            widget.setDisabled(True)
                            widget.disconnect()
                            break

    def filter_genre(self):
        self.genre = self.box_genre.currentData()
        self.populate_grid()

    def set_sorting(self):
        self.sorting = self.box_sort.currentData()
        self.populate_grid()

    def search_by_name(self):
        pass

    def play_station(self):
        station = self.sender().property("station")
        self.nativeParentWidget().add_and_show_widget(self.player)
        self.player.change_station(station=station)

    def setup_ui(self):
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(110, 130, 841, 431))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(20, 0, 221, 81))
        self.label_logo.setStyleSheet("image: url(:/icons/logo.png);")
        self.label_logo.setText("")

        self.box_genre = QtWidgets.QComboBox(self.centralwidget)
        self.box_genre.setGeometry(QtCore.QRect(540, 60, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.box_genre.setFont(font)
        self.box_genre.setStyleSheet("QComboBox\n"
                                     "{\n"
                                     "    color:white;\n"
                                     "    background-color: qlineargradient(x1:0, y1:0, x2:1,y2:1, stop: 1 rgba(94, 136, 161, 200), stop: 0 rgba(94, 136, 161, 200));\n"
                                     "    border-color: white;\n"
                                     "    border-width: 1px;\n"
                                     "    border-style: solid;\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "QComboBox::drop-down\n"
                                     "{\n"
                                     "    width: 35px;\n"
                                     "    border: 5px;\n"
                                     "    border-color:white;\n"
                                     "    border-left-style:solid;\n"
                                     "    border-top-style: none;\n"
                                     "    border-bottom-style: none;\n"
                                     "    border-right-style: none;\n"
                                     "}\n"
                                     "\n"
                                     "QComboBox::down-arrow\n"
                                     "{\n"
                                     "    \n"
                                     "    image: url(:/icons/down.png);\n"
                                     "    width: 25px;\n"
                                     "    height: 25px;\n"
                                     "}")

        self.box_sort = QtWidgets.QComboBox(self.centralwidget)
        self.box_sort.setGeometry(QtCore.QRect(780, 60, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.box_sort.setFont(font)
        self.box_sort.setStyleSheet("QComboBox\n"
                                    "{\n"
                                    "    color:white;\n"
                                    "    background-color: qlineargradient(x1:0, y1:0, x2:1,y2:1, stop: 1 rgba(94, 136, 161, 200), stop: 0 rgba(94, 136, 161, 200));\n"
                                    "    border-color: white;\n"
                                    "    border-width: 1px;\n"
                                    "    border-style: solid;\n"
                                    "}\n"
                                    "\n"
                                    "\n"
                                    "QComboBox::drop-down\n"
                                    "{\n"
                                    "    width: 35px;\n"
                                    "    border: 5px;\n"
                                    "    border-color:white;\n"
                                    "    border-left-style:solid;\n"
                                    "    border-top-style: none;\n"
                                    "    border-bottom-style: none;\n"
                                    "    border-right-style: none;\n"
                                    "}\n"
                                    "\n"
                                    "QComboBox::down-arrow\n"
                                    "{\n"
                                    "    \n"
                                    "    image: url(:/icons/down.png);\n"
                                    "    width: 25px;\n"
                                    "    height: 25px;\n"
                                    "}")

        self.btn_next = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.btn_next.setStyleSheet("QToolButton{\n"
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
        icon6.addPixmap(QtGui.QPixmap(":icons/forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_next.setIcon(icon6)
        self.btn_next.setIconSize(QtCore.QSize(60, 60))

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(320, 60, 201, 51))
        self.lineEdit.setStyleSheet("QLineEdit\n"
                                    "{\n"
                                    "    color:black;\n"
                                    "    border-color: rgba(94, 136, 161, 200);\n"
                                    "    border-width: 1px;\n"
                                    "    border-style: solid;\n"
                                    "}\n"
                                    "\n"
                                    "")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(480, 80, 31, 21))
        self.label.setStyleSheet("image: url(:/icons/search.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.toolButton_fav1_2 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_2.setEnabled(True)
        self.toolButton_fav1_2.setStyleSheet("QToolButton{\n"
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
        icon.addPixmap(QtGui.QPixmap(":icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_fav1_2.setIcon(icon)
        self.toolButton_fav1_2.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_2.setObjectName("toolButton_fav1_2")
        self.gridLayout.addWidget(self.toolButton_fav1_2, 0, 2, 1, 1)
        self.toolButton_fav1_10 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_10.setEnabled(True)
        self.toolButton_fav1_10.setStyleSheet("QToolButton{\n"
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
        self.toolButton_fav1_10.setIcon(icon1)
        self.toolButton_fav1_10.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_10.setObjectName("toolButton_fav1_10")
        self.gridLayout.addWidget(self.toolButton_fav1_10, 2, 1, 1, 1)

        self.btn_prev = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.btn_prev.setStyleSheet("QToolButton{\n"
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
        icon2.addPixmap(QtGui.QPixmap(":icons/backward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_prev.setIcon(icon2)
        self.btn_prev.setIconSize(QtCore.QSize(60, 60))
        self.gridLayout.addWidget(self.btn_prev, 1, 0, 1, 1)

        self.toolButton_fav1_9 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_9.setEnabled(True)
        self.toolButton_fav1_9.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_fav1_9.setIcon(icon1)
        self.toolButton_fav1_9.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_9.setObjectName("toolButton_fav1_9")
        self.gridLayout.addWidget(self.toolButton_fav1_9, 2, 2, 1, 1)
        self.toolButton_fav1_6 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_6.setEnabled(True)
        self.toolButton_fav1_6.setStyleSheet("QToolButton{\n"
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
        icon3.addPixmap(QtGui.QPixmap(":icons/fav4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_fav1_6.setIcon(icon3)
        self.toolButton_fav1_6.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_6.setObjectName("toolButton_fav1_6")
        self.gridLayout.addWidget(self.toolButton_fav1_6, 0, 4, 1, 1)
        self.toolButton_fav1_8 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_8.setEnabled(True)
        self.toolButton_fav1_8.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_fav1_8.setIcon(icon1)
        self.toolButton_fav1_8.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_8.setObjectName("toolButton_fav1_8")
        self.gridLayout.addWidget(self.toolButton_fav1_8, 2, 3, 1, 1)
        self.toolButton_fav1_14 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_14.setEnabled(True)
        self.toolButton_fav1_14.setStyleSheet("QToolButton{\n"
                                              "border: none ;\n"
                                              "background: transparent ;\n"
                                              "}\n"
                                              "\n"
                                              "QToolButton:pressed{\n"
                                              "background-color : rgb(255, 255, 255)\n"
                                              "}\n"
                                              "\n"
                                              "")
        self.toolButton_fav1_14.setIcon(icon1)
        self.toolButton_fav1_14.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_14.setObjectName("toolButton_fav1_14")
        self.gridLayout.addWidget(self.toolButton_fav1_14, 1, 5, 1, 1)
        self.toolButton_fav1_15 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_15.setEnabled(True)
        self.toolButton_fav1_15.setStyleSheet("QToolButton{\n"
                                              "border: none ;\n"
                                              "background: transparent ;\n"
                                              "}\n"
                                              "\n"
                                              "QToolButton:pressed{\n"
                                              "background-color : rgb(255, 255, 255)\n"
                                              "}\n"
                                              "\n"
                                              "")
        self.toolButton_fav1_15.setIcon(icon1)
        self.toolButton_fav1_15.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_15.setObjectName("toolButton_fav1_15")
        self.gridLayout.addWidget(self.toolButton_fav1_15, 2, 5, 1, 1)
        self.toolButton_fav1_13 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_13.setEnabled(True)
        self.toolButton_fav1_13.setStyleSheet("QToolButton{\n"
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
        icon4.addPixmap(QtGui.QPixmap(":icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_fav1_13.setIcon(icon4)
        self.toolButton_fav1_13.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_13.setObjectName("toolButton_fav1_13")
        self.gridLayout.addWidget(self.toolButton_fav1_13, 0, 5, 1, 1)
        self.toolButton_fav1_12 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_12.setEnabled(True)
        self.toolButton_fav1_12.setStyleSheet("QToolButton{\n"
                                              "border: none ;\n"
                                              "background: transparent ;\n"
                                              "}\n"
                                              "\n"
                                              "QToolButton:pressed{\n"
                                              "background-color : rgb(255, 255, 255)\n"
                                              "}\n"
                                              "\n"
                                              "")
        self.toolButton_fav1_12.setIcon(icon1)
        self.toolButton_fav1_12.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_12.setObjectName("toolButton_fav1_12")
        self.gridLayout.addWidget(self.toolButton_fav1_12, 2, 4, 1, 1)
        self.toolButton_fav1_7 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_7.setEnabled(True)
        self.toolButton_fav1_7.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_fav1_7.setIcon(icon1)
        self.toolButton_fav1_7.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_7.setObjectName("toolButton_fav1_7")
        self.gridLayout.addWidget(self.toolButton_fav1_7, 1, 2, 1, 1)
        self.toolButton_fav1_3 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_3.setEnabled(True)
        self.toolButton_fav1_3.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_fav1_3.setIcon(icon1)
        self.toolButton_fav1_3.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_3.setObjectName("toolButton_fav1_3")
        self.gridLayout.addWidget(self.toolButton_fav1_3, 1, 1, 1, 1)
        self.toolButton_fav1_4 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_4.setEnabled(True)
        self.toolButton_fav1_4.setStyleSheet("QToolButton{\n"
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
        icon5.addPixmap(QtGui.QPixmap(":icons/fav3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_fav1_4.setIcon(icon5)
        self.toolButton_fav1_4.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_4.setObjectName("toolButton_fav1_4")
        self.gridLayout.addWidget(self.toolButton_fav1_4, 0, 3, 1, 1)
        self.toolButton_fav1_5 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_5.setEnabled(True)
        self.toolButton_fav1_5.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_fav1_5.setIcon(icon1)
        self.toolButton_fav1_5.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_5.setObjectName("toolButton_fav1_5")
        self.gridLayout.addWidget(self.toolButton_fav1_5, 1, 3, 1, 1)

        self.gridLayout.addWidget(self.btn_next, 1, 6, 1, 1)
        self.toolButton_fav1 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1.setEnabled(True)
        self.toolButton_fav1.setStyleSheet("QToolButton{\n"
                                           "border: none ;\n"
                                           "background: transparent ;\n"
                                           "}\n"
                                           "\n"
                                           "QToolButton:pressed{\n"
                                           "background-color : rgb(255, 255, 255)\n"
                                           "}\n"
                                           "\n"
                                           "")
        self.toolButton_fav1.setIcon(icon1)
        self.toolButton_fav1.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1.setObjectName("toolButton_fav1")
        self.gridLayout.addWidget(self.toolButton_fav1, 0, 1, 1, 1)
        self.toolButton_fav1_11 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_fav1_11.setEnabled(True)
        self.toolButton_fav1_11.setStyleSheet("QToolButton{\n"
                                              "border: none ;\n"
                                              "background: transparent ;\n"
                                              "}\n"
                                              "\n"
                                              "QToolButton:pressed{\n"
                                              "background-color : rgb(255, 255, 255)\n"
                                              "}\n"
                                              "\n"
                                              "")
        self.toolButton_fav1_11.setIcon(icon1)
        self.toolButton_fav1_11.setIconSize(QtCore.QSize(120, 120))
        self.toolButton_fav1_11.setObjectName("toolButton_fav1_11")
        self.gridLayout.addWidget(self.toolButton_fav1_11, 1, 4, 1, 1)
