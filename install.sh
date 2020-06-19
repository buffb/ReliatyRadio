#!/usr/bin/env bash

####Dependency installation

sudo apt-get update &&
sudo apt-get upgrade -y &&
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox \
python3-pip python-setuptools python-wheel python3-pyqt5 python3-rpi.gpio git vlc -y
cd /opt/ || exit 1
sudo git clone https://github.com/buffb/ReliatyRadio.git
cd ReliatyRadio/ || exit 1
sudo -H pip3 install -r requirements.txt


#####Configuration
echo 'Configuring the ReliatyRadio'
sudo sed -i '$ a xset s off\nxset s noblank\nxset -dpms' /etc/xdg/openbox/autostart #disable display timeout aka screensaver
sudo sed -i '$ a sudo python3 /opt/ReliatyRadio/ReliatyRadio.py &' /etc/xdg/openbox/autostart # Radio autostart
sudo sed -i -e '$i startx &' /etc/rc.local # Run startx in rc.local
# Configure xinitrc
sudo sed -i -e '/.\/etc/ s/^#*/#/' /etc/X11/xinit/xinitrc # Comment out unnecessary lines
sudo sed -i -e '$ a exec openbox-session' /etc/X11/xinit/xinitrc

#Auto-Login without raspi-config
USER=${SUDO_USER:-$(who -m | awk '{ print $1 }')}
sudo systemctl set-default multi-user.target
sudo ln -fs /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@tty1.service
sudo cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I \$TERM
EOF

exit 0
