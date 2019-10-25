#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################
# Whatchdog for monitoring Raspberry Pi GPIO Status
# even a defined event occured on one or more inputs / outputs, a pyqtSignal will be emitted.
# for example, see Window-Class at the end of this file
#
# IMPORTANT: This script has to be executed as root, use sudo or gksudo
################################

import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, QThread, Qt

import logging
import time

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication

logger = logging.getLogger(__name__)

pins_in_use = {}
PIN_A = 3
PIN_B = 5


class GpioWatchdog(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.gpio_states = {}
        self.initReady = False
        self.__initGPIOs()
        self.rswitch = RotaryEncoder(PIN_A, PIN_B, None, self.switch_event, parent=self)
        self.initReady = True
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(lambda: self.assure_gpio_states_are_resetted())

    def __initGPIOs(self):
        # setup GPIO using Board numbering (pins, not GPIOs)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        # setup defined pins and event_detectors or outputs and initial states (initial is always 0, low)
        for pin in pins_in_use:
            if pins_in_use[pin][0] == GPIO.IN:
                if pin == 5:
                    GPIO.setup(pin, pins_in_use[pin][0], pull_up_down=GPIO.PUD_UP)
                else:
                    GPIO.setup(pin, pins_in_use[pin][0])
                GPIO.add_event_detect(pin, pins_in_use[pin][1], callback=self.shoutItOut, bouncetime=100)
                self.gpio_states.update({pin: 1})
            elif pins_in_use[pin][0] == GPIO.OUT:
                GPIO.setup(pin, pins_in_use[pin][0], initial=0)

    def shoutItOut(self, channel):
        logger.info("Channel: {0}, got falling Flank".format(channel))

        self.reset_timer.stop()
        if not self.initReady:
            logger.info("Channel: {0}, ignoring because of init not ready".format(channel))
            return
        force_newState = None
        activated = 0
        for i in range(10):
            time.sleep(.001)
            activated += GPIO.input(channel)
            print(activated)
        if activated is 10:
            force_newState = 1
            # logger.debug("new State is 1, because all measured values were 1")
        elif activated < 5:
            force_newState = 0
            # logger.debug("new State is 0, because all measured values were 0")

        if channel in self.gpio_states:
            lastState = self.gpio_states[channel]
            if force_newState is not None:
                if lastState is force_newState:
                    logger.debug("ignoring, because of force {0}".format(force_newState))
                    return
                newState = force_newState
            else:
                if lastState == 0:
                    newState = 1
                else:
                    newState = 0
            self.gpio_states.update({channel: newState})  # only inputs are included in this dict.

            if self.gpio_states[channel] == 1:
                self.emit(pyqtSignal("gpio_button_released"), channel)
            else:
                self.emit(pyqtSignal("gpio_button_pressed"), channel)

            self.reset_timer.start(5000)  # assure after 5 seconds, that last state is "released"
        return

    def assure_gpio_states_are_resetted(self):

        logger.debug("resetting last states of swithes")
        for entry in self.gpio_states.keys():
            self.gpio_states.update({entry: 1})  # Switches are 1 if the are released ....

    def switch_event(self, event):
        if event == RotaryEncoder.CLOCKWISE:
            self.emit(pyqtSignal("gpio_rotary_turned"), "clockwise")
            # print("clockwise")
        elif event == RotaryEncoder.ANTICLOCKWISE:
            self.emit(pyqtSignal("gpio_rotary_turned"), "anticlockwise")
            # print("anticlockwise")
        return

    def reset_gpios(self):
        self.initReady = False
        self.worker = None  # free worker for garbage collection
        GPIO.cleanup()


class RotaryEncoder:
    CLOCKWISE = 1
    ANTICLOCKWISE = 2
    BUTTONDOWN = 3
    BUTTONUP = 4
    rotary_a = 0
    rotary_b = 0
    rotary_c = 0
    last_state = 0
    direction = 0

    # Initialise rotary encoder object
    def __init__(self, pinA, pinB, button, callback, parent):
        self.pinA = pinA
        self.pinB = pinB
        self.button = button
        self.callback = callback
        self.parent = parent
        if self.pinA is not None and self.pinB is not None:
            GPIO.setmode(GPIO.BOARD)

            GPIO.setwarnings(False)
            GPIO.setup(self.pinA, GPIO.IN)
            GPIO.setup(self.pinB, GPIO.IN)
            GPIO.add_event_detect(self.pinA, GPIO.FALLING,
                                  callback=self.switch_event)
            GPIO.add_event_detect(self.pinB, GPIO.FALLING,
                                  callback=self.switch_event)

        if self.button is not None:
            GPIO.setup(self.button, GPIO.IN)
            GPIO.add_event_detect(self.button, GPIO.BOTH,
                                  callback=self.button_event, bouncetime=200)

        return
        # Call back routine called by switch events

    def switch_event(self, switch):
        if not self.parent.initReady:
            print("ignoring because init is not ready")
            return
        if GPIO.input(self.pinA):
            self.rotary_a = 1
        else:
            self.rotary_a = 0
        if GPIO.input(self.pinB):
            self.rotary_b = 1
        else:
            self.rotary_b = 0

        self.rotary_c = self.rotary_a ^ self.rotary_b
        new_state = self.rotary_a * 4 + self.rotary_b * 2 + self.rotary_c * 1
        delta = (new_state - self.last_state) % 4
        self.last_state = new_state
        event = 0
        if delta == 1:
            if self.direction == self.CLOCKWISE:
                # print "Clockwise"
                event = self.direction
            else:
                self.direction = self.CLOCKWISE
        elif delta == 3:
            if self.direction == self.ANTICLOCKWISE:
                # print "Anticlockwise"
                event = self.direction
            else:
                self.direction = self.ANTICLOCKWISE
        if event > 0:
            self.callback(event)
        return
        # Push button event

    def button_event(self, button):
        if GPIO.input(button):
            event = self.BUTTONUP
        else:
            event = self.BUTTONDOWN
        self.callback(event)
        return
        # Get a switch state

    def getSwitchState(self, switch):
        return GPIO.input(switch)


# End of RotaryEncoder class

class WorkerThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    # def __del__(self):
    #    self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        return


class MainWindow(QWidget):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.layout_window = QHBoxLayout()
        self.setLayout(self.layout_window)
        self.setFocus(Qt.NoFocusReason)

        self.gpio_watchdog = GpioWatchdog()

        self.connect(self.gpio_watchdog, pyqtSignal('gpio_button_pressed'),
                     self.pyqtSignalreader_buttons_on)  # carry pin no.
        self.connect(self.gpio_watchdog, pyqtSignal('gpio_button_released'),
                     self.pyqtSignalreader_buttons_off)  # carry pin no.
        self.connect(self.gpio_watchdog, pyqtSignal("gpio_rotary_turned"),
                     self.pyqtSignalreader_rotary)  # carry direction

    def pyqtSignalreader_buttons_on(self, channel):
        print("Pin {0} active".format(channel))
        for button in self.buttons:
            if int(button.text()) == channel:
                if not button.isChecked():
                    button.setChecked(True)
                else:
                    button.setChecked(False)

    def pyqtSignalreader_buttons_off(self, channel):
        print("Pin {0} inactive".format(channel))
        for button in self.buttons:
            if int(button.text()) == channel:
                if not button.isChecked():
                    button.setChecked(False)
                else:
                    button.setChecked(True)

    def pyqtSignalreader_rotary(self, direction):
        if direction is "clockwise":
            newRotary_value = self.rotary.value() + 1
            if newRotary_value > 100: newRotary_value = 100
            self.rotary.setValue(newRotary_value)
        elif direction is "anticlockwise":
            newRotary_value = self.rotary.value() - 1
            if newRotary_value < 0: newRotary_value = 0
            self.rotary.setValue(newRotary_value)

    def closeEvent(self, QCloseEvent):
        print("Cleanup GPIOs")
        self.gpio_watchdog.reset_gpios()
        QCloseEvent.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()
