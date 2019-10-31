import RPi.GPIO as GPIO
from Controller.GpioController import GpioController
import os, time


class PlayerGpioController():

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        self.controller = GpioController()
        self.controller.switch_callback = None
        self.controller.rotary_callback = self.rotaryChange
        self.controller.start()


    def readVolume(self):
        value = os.popen("amixer get PCM|grep -o [0-9]*%|sed 's/%//'").read()
        return int(value)

    def rotaryChange(self, direction):
        volume_step = 5
        volume = self.readVolume()
        if direction == 1:
            os.system("sudo amixer set PCM -- " + str(min(100, max(0, volume + volume_step))) + "%")
            print("vol-up")
        else:
            os.system("sudo amixer set PCM -- " + str(min(100, max(0, volume - volume_step))) + "%")
            print("vol-down")

    def start(self):
        self.controller.start()

    def stop(self):
        self.controller.stop()
