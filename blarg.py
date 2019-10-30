import time

from RPi import GPIO


def _clock_callback(self, pin):
    if GPIO.input(self.clock_pin) == 0:
        print(pin)
        self.rotary_callback(GPIO.input(self.data_pin))

if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)
    pin = 3
    GPIO.setup(pin, GPIO.IN)

    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(5, GPIO.RISING, callback=lambda r:_clock_callback(r), bouncetime=100)
    GPIO.add_event_detect(16, GPIO.RISING, callback=lambda r: _clock_callback(r),
                          bouncetime=100)


    while True:
        continue
    print("yay")
    GPIO.cleanup()
