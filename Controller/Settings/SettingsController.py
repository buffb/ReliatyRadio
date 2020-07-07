import os
import sys

from PyQt5 import QtCore
from wifi import Cell, Scheme

from Controller.Settings.SchemeWPA import SchemeWPA
from Controller.Update.ReliatyUpdater import ReliatyUpdater


class SettingsController(QtCore.QObject):
    status_updated = QtCore.pyqtSignal(str)
    ip_updated = QtCore.pyqtSignal(str)
    update_btn_updated = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, menu):
        super().__init__()
        self.menu = menu


    @QtCore.pyqtSlot(str,str)
    def connect_wifi(self, ssid, password):
        if ssid is not None:
            try:
                self.status_updated.emit("Verbinde..")
                cell = Cell.where("wlan0", lambda w: w.ssid == f"{ssid}")[0]
                if cell.encrypted is True and not password:
                    self.status_updated.emit("Passwort inkorrekt")
                    return
                scheme= SchemeWPA('wlan0',ssid,{"ssid":ssid,"psk":password})
                if scheme.iface in [iface.iface for iface in SchemeWPA.all()]:
                    scheme.delete()
                scheme.save()

                scheme.activate()
                self.status_updated.emit(self.get_status())
                self.ip_updated.emit(self.get_ip())

            except IndexError:
                self.status_updated.emit("Netzwerk nicht gefunden")
            except:
                self.status_updated.emit("Fehler bei der Verbindungsaufnahme")
                e = sys.exc_info()[0]
                pass
            finally:
                self.finished.emit()

    @QtCore.pyqtSlot()
    def update_software(self):
        self.update_btn_updated.emit("Suche nach Updates..")
        updater = ReliatyUpdater()
        if updater.check_for_update():
            self.update_btn_updated.emit("Downloade Update..")
            success = updater.do_update()
            if success:
                self.restart()
            self.update_btn_updated.emit("Fehler beim Update")
            return
        self.update_btn_updated.emit("Keine Updates verfügbar")
        self.finished.emit()

    def restart(self):
        import subprocess
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def get_status(self):
        status = "Nicht verbunden"
        if os.popen('ip addr show wlan0').read().__contains__("state UP") and self.get_ip():
            status = "Verbunden (" + os.popen('iwgetid').read().split('"')[1]+ ")"
        return status

    def get_ip(self):
        try:
            ip = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
        except IndexError:
            return ""
        return ip
