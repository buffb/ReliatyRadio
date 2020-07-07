from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, Qt

from Controller.Settings.SettingsController import SettingsController


class SettingsMenu(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.setup_ui()
        self.thread = QThread()
        self.controller = SettingsController(self)

        #Connect slots
        self.controller.status_updated.connect(self.update_status)
        self.controller.ip_updated.connect(self.update_ip)
        self.controller.update_btn_updated.connect(self.update_update_btn)

        self.btn_wifi__connect.clicked.connect(self.connect_to_wifi)
        self.btn_update.clicked.connect(self.check_for_update)

        self.btn_home.clicked.connect(self.go_home)

        #Start Background Worker
        self.controller.moveToThread(self.thread)
        self.thread.start()
        self.controller.finished.connect(self.thread.quit)

        self.update_status(self.controller.get_status())
        self.update_ip(self.controller.get_ip())

    def go_home(self):
        self.thread.exit(0)
        self.nativeParentWidget().show_main_menu()


    def connect_to_wifi(self):
        self.thread.start()
        QtCore.QMetaObject.invokeMethod(self.controller,"connect_wifi", Qt.QueuedConnection,
                                        QtCore.Q_ARG(str, self.ssid_input.text()),
                                        QtCore.Q_ARG(str, self.wifi_pwd_input.text()))

    def check_for_update(self):
        QtCore.QMetaObject.invokeMethod(self.controller,"update_software", Qt.QueuedConnection)
        #Will not excecute if restarted after update was necessary
        self.btn_update.setEnabled(False)

    def update_status(self,status):
        self.label_status2.setText(status)

    def update_ip(self,ip):
        self.label_ip2.setText(ip)

    def update_update_btn(self,text):
        self.btn_update.setText(text)


    def setup_ui(self):
        self.setEnabled(True)

        font = QtGui.QFont()
        font.setPointSize(12)

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


        ###WIFI Section

        self.wifisection = QtWidgets.QWidget(self.centralwidget)
        self.wifisection.setGeometry(QtCore.QRect(10, 100, 300, 200))
        self.wifisection.setObjectName("wifisection")
        self.wifiLayout = QtWidgets.QGridLayout(self.wifisection)
        self.wifiLayout.setContentsMargins(0, 0, 0, 0)
        self.wifiLayout.setObjectName("wifiLayout")


        self.wifi_icon_label = QtWidgets.QLabel(self.wifisection)
        self.wifi_icon_label.setWordWrap(False)
        self.wifi_icon_label.setObjectName("wifi_icon_label")
        pixmap = QtGui.QPixmap(":/icons/wlan.png")
        self.wifi_icon_label.resize(40,40)
        self.wifi_icon_label.setPixmap(pixmap.scaled(self.wifi_icon_label.size(), QtCore.Qt.KeepAspectRatio))
        self.wifiLayout.addWidget(self.wifi_icon_label, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)




        #Connection State Labels

        self.label_status1 = QtWidgets.QLabel("Status:", self.wifisection)
        self.label_status2 = QtWidgets.QLabel("", self.wifisection)
        self.label_ip1 = QtWidgets.QLabel("IP Adresse:", self.wifisection)
        self.label_ip2 = QtWidgets.QLabel("", self.wifisection)
        self.label_status1.setObjectName("label_status1")
        self.label_status2.setObjectName("label_status2")
        self.label_ip1.setObjectName("label_ip1")
        self.label_ip2.setObjectName("label_ip2")
        self.label_status1.setFont(font)
        self.label_status2.setFont(font)
        self.label_ip1.setFont(font)
        self.label_ip2.setFont(font)
        self.wifiLayout.addWidget(self.label_status1, 1, 0, 1, 1)
        self.wifiLayout.addWidget(self.label_status2, 1, 1, 1, 1)
        self.wifiLayout.addWidget(self.label_ip1, 2, 0, 1, 1)
        self.wifiLayout.addWidget(self.label_ip2, 2, 1, 1, 1)

        #SSID Input
        self.ssid_input = QtWidgets.QLineEdit(self.wifisection)
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
        self.wifiLayout.addWidget(self.ssid_input, 3, 1, 1, 1)
        self.ssid_label = QtWidgets.QLabel("SSID", self.wifisection)
        self.ssid_label.setFont(font)
        self.wifiLayout.addWidget(self.ssid_label, 3, 0, 1, 1)

        #Password Input
        self.wifi_pwd_input = QtWidgets.QLineEdit(self.wifisection)
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
        self.wifiLayout.addWidget(self.wifi_pwd_input, 4, 1, 1, 1)

        self.password_label = QtWidgets.QLabel("Passwort", self.wifisection)
        self.password_label.setObjectName("label_2")
        self.password_label.setFont(font)
        self.wifiLayout.addWidget(self.password_label, 4, 0, 1, 1)

        self.btn_wifi__connect = QtWidgets.QToolButton(self.wifisection)
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
        self.wifiLayout.addWidget(self.btn_wifi__connect, 6, 0, 1, 2, QtCore.Qt.AlignRight)

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
        self.btn_update.setFont(font)
