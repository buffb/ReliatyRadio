# Form implementation generated from reading ui file 'Player.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
import time

import vlc
from PyQt5 import QtCore, QtGui, QtWidgets


class WebradioPlayer(QtWidgets.QWidget):

    def __init__(self, parent=None, webradio=None):
        super().__init__(parent)
        self.setupUi()
        self.name = webradio.name
        self.url = webradio.url
        #self.icon =webradio.icon

        self.player = vlc.MediaPlayer(self.url)

    def open_stream(self):
        """Opens the radio stream
        """
        # Set the title of the track as window title
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for thi

        self.player.play()
        time.sleep(20)

    def setupUi(self):
        self.setObjectName("Webradio Player")
        self.frame_music_control = QtWidgets.QFrame(self)
        self.frame_music_control.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_music_control.sizePolicy().hasHeightForWidth())
        self.frame_music_control.setSizePolicy(sizePolicy)
        self.frame_music_control.setMinimumSize(QtCore.QSize(400, 271))
        self.frame_music_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_music_control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_music_control.setObjectName("frame_music_control")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_music_control)
        self.gridLayout.setContentsMargins(40, -1, 40, -1)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 1)
        self.lbl_duration = QtWidgets.QLabel(self.frame_music_control)
        self.lbl_duration.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lbl_duration.setObjectName("lbl_duration")
        self.gridLayout.addWidget(self.lbl_duration, 8, 2, 1, 1)
        self.lbl_playtime = QtWidgets.QLabel(self.frame_music_control)
        self.lbl_playtime.setObjectName("lbl_playtime")
        self.gridLayout.addWidget(self.lbl_playtime, 8, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.frame_music_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMaximumSize(QtCore.QSize(200, 200))
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
        self.lbl_nowplaying = QtWidgets.QLabel(self.frame_music_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_nowplaying.sizePolicy().hasHeightForWidth())
        self.lbl_nowplaying.setSizePolicy(sizePolicy)
        self.lbl_nowplaying.setObjectName("lbl_nowplaying")
        self.gridLayout.addWidget(self.lbl_nowplaying, 3, 1, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizontalSlider = QtWidgets.QSlider(self.frame_music_control)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 6, 1, 1, 1)
        self.lbl_station = QtWidgets.QLabel(self.frame_music_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_station.sizePolicy().hasHeightForWidth())
        self.lbl_station.setSizePolicy(sizePolicy)
        self.lbl_station.setObjectName("lbl_station")
        self.gridLayout.addWidget(self.lbl_station, 2, 1, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.frame_2 = QtWidgets.QFrame(self.frame_music_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(980, 0))
        self.frame_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setHorizontalSpacing(19)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.frame_2)
        self.toolButton_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy)
        self.toolButton_3.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton_3.setMaximumSize(QtCore.QSize(20, 20))
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout_2.addWidget(self.toolButton_3, 0, 1, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.toolButton_2 = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        self.toolButton_2.setMinimumSize(QtCore.QSize(60, 60))
        self.toolButton_2.setMaximumSize(QtCore.QSize(40, 40))
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout_2.addWidget(self.toolButton_2, 0, 2, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.toolButton = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton.setMaximumSize(QtCore.QSize(20, 20))
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.toolButton, 0, 3, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 9, 1, 1, 1)
        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_duration.setText(_translate("MainWindow", "0:00"))
        self.lbl_playtime.setText(_translate("MainWindow", "0:00"))
        self.lbl_nowplaying.setText(_translate("MainWindow", "<html><head/><body><p>Now Playing</p></body></html>"))
        self.lbl_station.setText(_translate("MainWindow", "<html><head/><body><p>Station Name</p></body></html>"))
        self.toolButton_3.setText(_translate("MainWindow", "..."))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.toolButton.setText(_translate("MainWindow", "..."))
