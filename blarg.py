import time

from RPi import GPIO

if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)
    pin = 12
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == GPIO.LOW:
        print("nay")
        continue
    print("yay")
    GPIO.cleanup()
