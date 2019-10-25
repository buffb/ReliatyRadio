from RPi import GPIO

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    pin = 32
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == GPIO.LOW:
        continue
    print("yay")

# 7 = Sensing
# 11 = Impedance
# 8 - Rot
# 10 Grün
# 12 Threshold
# 32 Power
