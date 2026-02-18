from gpiozero import LED
from time import sleep

r1=
while True:
	
	led1.on()

	sleep(1)
	led1.off()

	sleep(1)



r1.off()
r2.off()
r3.off()
r4.off()
y1.off()
y2.off()
y3.off()
y4.off()
g1.off()
g2.off()
g3.off()
g4.off()


while True:
	g1.on()
	r2.on()
	r4.on()
	sleep(3)
	
	
	g1.off()
	y1.on()
	sleep(1)
	
	
	y1.off()
	g2.on()
	r1.on()
	r3.on()
	r4.on()
	sleep(3)
	
	g2.off()
	y2.on()
	sleep(1)
	
	
	y2.off()
	g3.on()
	r1.on()
	r2.on()
	sleep(3)
	
	g3.off()
	y3.on()
	sleep(1)
	
	
	y2.off()
	g4.on()
	r1.on()
	r2.on()
	r3.on()
	sleep(3)
	
	g4.off()
	y4.on()
	sleep(1)
	
	y4.off()
	r4.on()
	r1.on()
	r2.on()
	sleep(3)


