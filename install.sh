#!/usr/bin/env bash

####Dependency installation

sudo apt-get update &&
sudo apt-get upgrade -y &&
sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox \
python3-pip python-setuptools python-wheel python3-pyqt5 python3-rpi.gpio git vlc omxplayer -y
cd /opt/ || exit 1
sudo git clone https://github.com/buffb/ReliatyRadio.git
cd ReliatyRadio/ || exit 1
sudo -H pip3 install -r requirements.txt


#####Configuration
echo 'Configuring the ReliatyRadio'
sudo sed -i '$ a xset s off\nxset s noblank\nxset -dpms' /etc/xdg/openbox/autostart
sudo sed -i '$ a omxplayer /opt/ReliatyRadio/Resources/intro.mp4' /etc/xdg/openbox/autostart #disable display timeout aka screensaver
sudo sed -i '$ a sudo python3 /opt/ReliatyRadio/ReliatyRadio.py &' /etc/xdg/openbox/autostart # Radio autostart
sudo sed -i -e '$i startx &' /etc/rc.local # Run startx in rc.local
# Configure xinitrc
sudo sed -i -e '/.\/etc/ s/^#*/#/' /etc/X11/xinit/xinitrc # Comment out unnecessary lines
sudo sed -i -e '$ a exec openbox-session' /etc/X11/xinit/xinitrc

#Set Audio Jack to default sound card
sudo tee -a /etc/asound.conf << END
defaults.pcm.card 1
defaults.ctl.card 1
END

#Rotate display and touch input
sudo sed -i '/touchscreen catchall.*/a \\tOption "TransformationMatrix" "-1 0 1 0 -1 1 0 0 1"' /usr/share/X11/xorg.conf.d/40-libinput.conf
sudo sed -i -e '$ a hdmi_cvt 1024 600 60' /boot/config.txt
sudo sed -i -e '$ a display_rotate=2' /boot/config.txt

#German Keyboard
sudo sed -i  "s/XKBLAYOUT=../XKBLAYOUT=de/g" /etc/default/keyboard

#Disable ipv6
sudo sed -i -e '$ a net.ipv6.conf.all.disable_ipv6 = 1' /etc/sysctl.conf
exit 0
