from gpiozero import LED
from time import sleep

# Define traffic light GPIO pins for each direction
NORTH = {'RED': 2, 'YELLOW': 4, 'GREEN': 15}
EAST  = {'RED': 18, 'YELLOW': 22, 'GREEN': 10}
SOUTH = {'RED': 25, 'YELLOW': 8, 'GREEN': 0}
WEST  = {'RED': 5, 'YELLOW': 12, 'GREEN': 13}

# Create LED objects for each light
r1, y1, g1 = LED(NORTH['RED']), LED(NORTH['YELLOW']), LED(NORTH['GREEN'])
r2, y2, g2 = LED(EAST['RED']), LED(EAST['YELLOW']), LED(EAST['GREEN'])
r3, y3, g3 = LED(SOUTH['RED']), LED(SOUTH['YELLOW']), LED(SOUTH['GREEN'])
r4, y4, g4 = LED(WEST['RED']), LED(WEST['YELLOW']), LED(WEST['GREEN'])

# Turn off all LEDs initially
all_leds = [r1, y1, g1, r2, y2, g2, r3, y3, g3, r4, y4, g4]
for led in all_leds:
    led.off()

print("Starting 4-way traffic light control...")

# Main loop for 4-way traffic control
while True:
    # NORTH direction go
    g1.on(); r2.on(); r3.on(); r4.on()
    sleep(3)
    g1.off(); y1.on()
    sleep(1)
    y1.off(); r1.on()

    # EAST direction go
    g2.on(); r1.on(); r3.on(); r4.on()
    sleep(3)
    g2.off(); y2.on()
    sleep(1)
    y2.off(); r2.on()

    # SOUTH direction go
    g3.on(); r1.on(); r2.on(); r4.on()
    sleep(3)
    g3.off(); y3.on()
    sleep(1)
    y3.off(); r3.on()

    # WEST direction go
    g4.on(); r1.on(); r2.on(); r3.on()
    sleep(3)
    g4.off(); y4.on()
    sleep(1)
    y4.off(); r4.on()
