from PyQt5 import QtWidgets

from View.Menus.MainMenu import MainMenu

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainMenu()
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
