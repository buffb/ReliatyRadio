import os
import sys

from PyQt5.QtCore import QObject, pyqtSignal
from wifi import Cell, Scheme

from Controller.Settings.SchemeWPA import SchemeWPA
from Controller.Update.ReliatyUpdater import ReliatyUpdater


class SettingsController(QObject):
    def __init__(self, menu):
        super().__init__()
        status_updated = pyqtSignal(str)
        intReady = pyqtSignal(int)
        self.menu = menu

    def connect_wifi(self, ssid, password):
        if ssid is not None:
            try:
                self.status_updated.emit("Verbinde..")
                cell = Cell.where("wlan0", lambda w: w.ssid == f"{ssid}")[0]
                if cell.encrypted is True and not password:
                    self.menu.label_status2.setText("Passwort inkorrekt")
                    return
                scheme= SchemeWPA('wlan0',ssid,{"ssid":ssid,"psk":password})
                if scheme.iface in [iface.iface for iface in SchemeWPA.all()]:
                    scheme.delete()
                scheme.save()

                scheme.activate()

                self.menu.populate_labels()


            except IndexError:
                self.menu.label_status2.setText("Netzwerk nicht gefunden")
            except:
                e = sys.exc_info()[0]
                pass

    def update_software(self):
        self.menu.update_btn.setText("Suche nach Updates..")
        updater = ReliatyUpdater()
        if updater.check_for_update():
            success = updater.do_update()
            if success:
                self.restart()

        return False

    def restart(self):
        import subprocess
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def get_status(self):
        status = "Nicht verbunden"
        if os.popen('ip addr show wlan0').read().__contains__("state UP"):
            status = "Verbunden (" + os.popen('iwgetid').read().split('"')[1]+ ")"
        return status

    def get_ip(self):
        ip = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
        return ip
