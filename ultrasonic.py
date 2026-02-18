from gpiozero import DistanceSensor, LED
from time import sleep

sensor = DistanceSensor(echo=21, trigger=20)
led1 = LED(27)
led2 = LED(17)

while True:
	distance = sensor.distance*100
	print("distance :",distance)
	
	if distance < 5:
		led2.on()
	else:
		led2.off()
		
	if distance > 20:
		led1.on()
	else:
		led1.off()
	sleep(1)
