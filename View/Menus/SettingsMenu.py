from PyQt5 import QtCore, QtGui, QtWidgets
from wifi import Cell

from Controller.Settings.SchemeWPA import SchemeWPA
from Settings.SettingsController import SettingsController


class SettingsMenu(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.controller = SettingsController()

        self.btn_wifi__connect.clicked.connect(lambda: self.controller.connect_wifi(self.ssid_input.text(),
                                                                                    self.wifi_pwd_input.text()))
        self.btn_update.clicked.connect(self.check_for_update)


    def check_for_update(self):
        self.controller.update_software()
        #Will not excecute if restarted after update was necessary
        self.btn_update.setEnabled(False)
        self.btn_update.setText("Kein Update verfügbar")

    def setup_ui(self):
        self.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/radio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setToolTipDuration(-5)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 1024, 768))

        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(100, 10, 221, 81))
        self.label_logo.setStyleSheet("image: url(:/icons/logo.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.btn_home = QtWidgets.QToolButton(self.centralwidget)
        self.btn_home.setGeometry(QtCore.QRect(10, 10, 81, 71))
        self.btn_home.setStyleSheet("QToolButton{\n"
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
        icon.addPixmap(QtGui.QPixmap(":icons/home.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btn_home.setIcon(icon)
        self.btn_home.setIconSize(QtCore.QSize(40, 40))
        self.btn_home.setObjectName("toolButton_home")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 100, 311, 163))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_logo_2 = QtWidgets.QLabel(self.widget)
        self.label_logo_2.setStyleSheet("image: url(:/icons/wlan.png);")
        self.label_logo_2.setText("")
        self.label_logo_2.setWordWrap(False)
        self.label_logo_2.setObjectName("label_logo_2")
        self.gridLayout.addWidget(self.label_logo_2, 1, 1, 1, 1)
        self.ssid_input = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ssid_input.setFont(font)
        self.ssid_input.setStyleSheet("QLineEdit\n"
                                      "{\n"
                                      "    color:black;\n"
                                      "    border-color: rgba(94, 136, 161, 200);\n"
                                      "    border-width: 1px;\n"
                                      "    border-style: solid;\n"
                                      "}\n"
                                      "@label->setStyleSheet(\"font: 18pt;\");\n"
                                      "")
        self.ssid_input.setText("")
        self.ssid_input.setFrame(True)
        self.ssid_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.ssid_input.setClearButtonEnabled(False)
        self.ssid_input.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.ssid_input, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel("SSID", self.widget)
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel("Passwort", self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.wifi_pwd_input = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.wifi_pwd_input.setFont(font)
        self.wifi_pwd_input.setStyleSheet("QLineEdit\n"
                                          "{\n"
                                          "    color:black;\n"
                                          "    border-color: rgba(94, 136, 161, 200);\n"
                                          "    border-width: 1px;\n"
                                          "    border-style: solid;\n"
                                          "}\n"
                                          "@label->setStyleSheet(\"font: 18pt;\");\n"
                                          "")
        self.wifi_pwd_input.setText("")
        self.wifi_pwd_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.wifi_pwd_input.setPlaceholderText("")
        self.wifi_pwd_input.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.wifi_pwd_input, 3, 1, 1, 1)
        self.btn_wifi__connect = QtWidgets.QToolButton(self.widget)
        self.btn_wifi__connect.setStyleSheet("QToolButton{\n"
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
        icon2.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_wifi__connect.setIcon(icon2)
        self.btn_wifi__connect.setIconSize(QtCore.QSize(40, 40))
        self.btn_wifi__connect.setObjectName("btn_wifi__connect")
        self.gridLayout.addWidget(self.btn_wifi__connect, 4, 1, 1, 1, QtCore.Qt.AlignRight)

        self.btn_update = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update.setGeometry(QtCore.QRect(780, 10, 231, 41))
        self.btn_update.setStyleSheet("QPushButton\n"
                                      "{\n"
                                      "    color:black;\n"
                                      "    border-color: rgba(94, 136, 161, 200);\n"
                                      "    border-width: 1px;\n"
                                      "    border-style: solid;\n"
                                      "}\n"
                                      "QPushButton:hover\n"
                                      "{\n"
                                      "   background-color:rgba(94, 136, 161, 200);\n"
                                      "}\n"
                                      "")
        self.btn_update.setObjectName("btn_update")
        self.btn_update.setText("Updates installieren")
