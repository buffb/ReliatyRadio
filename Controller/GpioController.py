
import RPi.GPIO as GPIO
from time import sleep


class GpioController:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    DEBOUNCE = 50
    DEBOUNCE_SWITCH = 1000

    # 7 = Sensing
    # 11 = Impedance
    # 8 - Rot
    # 10 Grün
    # 12 Threshold
    # 32 Power

    def __init__(self, 
                 clock_pin= 16,
                 data_pin = 5,
                 switch_pin = 3,


                 sensing_pin=7,
                 thresh_pin=12,
                 impedance_pin=11,
                 freeze_pin=13,
                 redbtn_pin=8,
                 greenbtn_pin=10,
                 onoff_pin=32,


                 rotary_callback=None,
                 switch_callback=None,
                 sensing_callback=None,
                 thresh_callback=None,
                 impedance_callback=None,
                 freeze_callback=None,
                 redbtn_callback=None,
                 greenbtn_callback=None,
                 onoff_callback=None):

        # persist values
        self.clock_pin = clock_pin
        self.data_pin = data_pin
        self.switch_pin = switch_pin
        self.sensing_pin = sensing_pin
        self.thresh_pin = thresh_pin
        self.impedance_pin = impedance_pin
        self.freeze_pin = freeze_pin
        self.redbtn_pin = redbtn_pin
        self.greenbtn_pin = greenbtn_pin
        self.onoff_pin_pin = onoff_pin

        self.rotary_callback = rotary_callback
        self.switch_callback = switch_callback
        self.sensing_callback = sensing_callback
        self.thresh_callback = thresh_callback
        self.impedance_callback = impedance_callback
        self.freeze_callback = freeze_callback
        self.redbtn_callback = redbtn_callback
        self.greenbtn_callback = greenbtn_callback
        self.onoff_callback = onoff_callback

        # setup pins
        GPIO.setup(self.clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.data_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.clock_pin, GPIO.FALLING, callback=self._clock_callback, bouncetime=self.DEBOUNCE)
        GPIO.add_event_detect(self.switch_pin, GPIO.FALLING, callback=self._switch_callback, bouncetime=self.DEBOUNCE_SWITCH)

    def stop(self):
        GPIO.remove_event_detect(self.clock_pin)
        GPIO.remove_event_detect(self.switch_pin)
        GPIO.cleanup()
    
    def _clock_callback(self, pin):
        if GPIO.input(self.clock_pin) == 0:
            self.rotary_callback(GPIO.input(self.data_pin))

    def _switch_callback(self, pin):
        if self.switch_callback is not None:
            self.switch_callback()
