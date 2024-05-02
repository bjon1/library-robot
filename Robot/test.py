from USensor import USensor
import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
trig = 23
echo = 24
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# start sensor
GPIO.output(trig, False)
print("Waiting for Ultrasound Sensor to Settle...")
time.sleep(2)
while True:
	
	# send pulse
	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)

	# receive response and calculate distance
	while GPIO.input(echo) == 0:
		t_start = time.time() 
	while GPIO.input(echo) == 1:
		t_end = time.time()
	t = t_end - t_start
	distance = (t * 17150) 
	distance = round(distance, 2)

	print(f"Distance: {distance} centimeters")
	time.sleep(1)

