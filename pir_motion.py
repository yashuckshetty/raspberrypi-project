from gpiozero import MotionSensor, LED
from time import sleep

led1 = LED(27)  # Example: BCM 27 corresponds to BOARD 13
led2 = LED(22)  # Example: BCM 22 corresponds to BOARD 15

# Initialize the PIR sensor on GPIO 17
pir = MotionSensor(17)

print("Waiting for PIR to settle...")
pir.wait_for_no_motion()

while True:
    pir.wait_for_motion()
    print("Motion detected!")
    led1.on()
    led2.on()
    sleep(1)

    pir.wait_for_no_motion()
    print("No motion")
    led1.off()
    led2.off()

