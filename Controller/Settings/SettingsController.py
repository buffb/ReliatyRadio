import os
import sys

from wifi import Cell

from Controller.Settings.SchemeWPA import SchemeWPA
from Controller.Update.ReliatyUpdater import ReliatyUpdater


class SettingsController:
    def __init__(self):
        return

    def connect_wifi(self, ssid, password):
        if ssid is not None:
            # Wrap into try except, because there is always an error thrown. Wifi should work nevertheless
            try:
                cell = Cell.where("wlan0", lambda w: w.ssid == f"{ssid}")[0]
                scheme = SchemeWPA('wlan0', cell.ssid, {"ssid": cell.ssid, "psk": f"{password}"})
                scheme.save()
                scheme.activate()
            except:
                pass

    def update_software(self):
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
