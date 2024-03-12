import Jetson.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(18, GPIO.IN, initial = GPIO.HIGH)
GPIO.setup(16, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(21, GPIO.IN, initial = GPIO.HIGH)
GPIO.setup(19, GPIO.OUT, initial = GPIO.HIGH)

#18 and 21 should be in but try out for now