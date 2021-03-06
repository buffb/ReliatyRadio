from PyQt5 import QtCore, QtGui, QtWidgets

from View.Menus.SettingsMenu import SettingsMenu
from View.ReliatyPlayer import ReliatyPlayer
from Resources.resources_rc import *


class MainMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.toolButton_settings.clicked.connect(self.show_settings)
        self.toolButton_player.clicked.connect(self.show_webradio)

    def setup_ui(self):

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/radio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setToolTipDuration(-5)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(self)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.toolButton_player = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton_player.setStyleSheet("QToolButton{\n"
                                             "border: none ;\n"
                                             "background: transparent ;\n"
                                             "}\n"
                                             "\n"
                                             "QToolButton:pressed{\n"
                                             "background-color : rgb(255, 255, 255)\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.toolButton_player.setIcon(icon)
        self.toolButton_player.setIconSize(QtCore.QSize(300, 300))
        self.toolButton_player.setObjectName("toolButton_player")
        self.horizontalLayout_2.addWidget(self.toolButton_player)

        self.toolButton_settings = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton_settings.setStyleSheet("QToolButton{\n"
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
        icon1.addPixmap(QtGui.QPixmap(":/icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_settings.setIcon(icon1)
        self.toolButton_settings.setIconSize(QtCore.QSize(300, 300))
        self.toolButton_settings.setObjectName("toolButton_settings")
        self.horizontalLayout_2.addWidget(self.toolButton_settings)

        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(20, 10, 411, 111))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setStyleSheet("image: url(:/icons/logo.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")



    def show_settings(self):
        widget = SettingsMenu()
        self.nativeParentWidget().add_and_show_widget(widget)


    def show_webradio(self):
        widget = ReliatyPlayer()
        self.nativeParentWidget().add_and_show_widget(widget)
