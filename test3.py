import RPi.GPIO as GPIO
import time
import threading
import requests
from RPLCD.i2c import CharLCD
import smtplib
from twilio.rest import Client

# ================= GPIO MODE =================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# ================= GPIO SETUP =================
RUN_LED = 27
IDLE_LED = 22
OFF_LED = 23
SWITCH_PIN = 24

GPIO.setup(RUN_LED, GPIO.OUT)
GPIO.setup(IDLE_LED, GPIO.OUT)
GPIO.setup(OFF_LED, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ================= LCD =================
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()

# ================= TIME COUNTERS =================
running_time = 0
idle_time = 0
off_time = 0
state = "OFF"
lock = threading.Lock()

# ================= THINGSPEAK =================
THINGSPEAK_API_KEY = "6HXLP6AFKZHUE30F"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ================= EMAIL =================
EMAIL_FROM = "poorviaadhya@gmail.com"
EMAIL_TO = "yashuckshetty@gmail.com"
EMAIL_APP_PASSWORD = "pyus benp mbzf vbdf"

def send_email_alert(subject, body):
    try:
        msg = f"Subject:{subject}\n\n{body}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg)
        server.quit()
        print("Email sent")
    except Exception as e:
        print("Email error:", e)

# ================= WHATSAPP (TWILIO) =================
account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"


client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp(key, level):
    try:
        message = client.messages.create(
            body=f"⚠️ ALERT!\nKey '{key}' pressed\nLevel {level} crossed threshold",
            from_="whatsapp:+14155238886",
            to="whatsapp:+917349675141"
        )

        print("WhatsApp request accepted")
        print("Message SID:", message.sid)
        print("Message Status:", message.status)

    except Exception as e:
        print("WhatsApp error:", e)

# ================= KEYPAD =================
KEYPAD = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

ROW_PINS = [5, 6, 13, 19]
COL_PINS = [12, 16, 20, 21]

for r in ROW_PINS:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.HIGH)

for c in COL_PINS:
    GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ================= THRESHOLD LOGIC =================
KEY_LEVELS = {
    '1': 1, '2': 2, '3': 3,
    '4': 4, '5': 5, '6': 6,
    'A': 7, 'B': 8
}

THRESHOLD_LEVEL = 5
whatsapp_sent = False

def scan_keypad():
    global whatsapp_sent

    while True:
        for i, row in enumerate(ROW_PINS):
            GPIO.output(row, GPIO.LOW)

            for j, col in enumerate(COL_PINS):
                if GPIO.input(col) == GPIO.LOW:
                    key = KEYPAD[i][j]
                    print("Key pressed:", key)

                    if key in KEY_LEVELS:
                        level = KEY_LEVELS[key]
                        print("Key level:", level)

                        if level >= THRESHOLD_LEVEL and not whatsapp_sent:
                            send_whatsapp(key, level)
                            whatsapp_sent = True

                    time.sleep(0.4)  # debounce

            GPIO.output(row, GPIO.HIGH)

        time.sleep(0.05)

# ================= LED UPDATE =================
def update_leds():
    GPIO.output(RUN_LED, state == "RUNNING")
    GPIO.output(IDLE_LED, state == "IDLE")
    GPIO.output(OFF_LED, state == "OFF")

# ================= LCD UPDATE =================
def update_lcd():
    total = running_time + idle_time + off_time
    utilization = int((running_time / total) * 100) if total > 0 else 0

    lcd.clear()
    lcd.write_string(f"STATE:{state}")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"U:{utilization}% R:{running_time}")

# ================= COUNTERS =================
def increment_counters():
    global running_time, idle_time, off_time, whatsapp_sent
    email_sent = False

    while True:
        time.sleep(1)
        with lock:
            if state == "RUNNING":
                running_time += 1
                email_sent = False

            elif state == "IDLE":
                idle_time += 1
                whatsapp_sent = False
                email_sent = False

            elif state == "OFF":
                off_time += 1
                whatsapp_sent = False
                if not email_sent:
                    send_email_alert("Machine OFF Alert", "Machine is in OFF state")
                    email_sent = True

            update_leds()
            update_lcd()

# ================= THINGSPEAK =================
def send_to_thingspeak():
    total = running_time + idle_time + off_time
    utilization = int((running_time / total) * 100) if total > 0 else 0

    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": running_time,
        "field2": idle_time,
        "field3": utilization
    }

    try:
        requests.post(THINGSPEAK_URL, data=data, timeout=5)
        print("ThingSpeak updated")
    except:
        print("ThingSpeak error")

def thingspeak_loop():
    while True:
        time.sleep(20)
        with lock:
            send_to_thingspeak()

# ================= KEYBOARD CONTROL =================
def keyboard_control():
    global state, whatsapp_sent
    print("Controls: r=RUN, i=IDLE, o=OFF, q=QUIT")

    while True:
        key = input().lower()
        with lock:
            if key == "r":
                state = "RUNNING"
            elif key == "i":
                state = "IDLE"
                whatsapp_sent = False
            elif key == "o":
                state = "OFF"
                whatsapp_sent = False
            elif key == "q":
                lcd.clear()
                GPIO.cleanup()
                exit()

# ================= THREADS =================
threading.Thread(target=increment_counters, daemon=True).start()
threading.Thread(target=thingspeak_loop, daemon=True).start()
threading.Thread(target=keyboard_control, daemon=True).start()
threading.Thread(target=scan_keypad, daemon=True).start()

# ================= MAIN LOOP =================
while True:
    time.sleep(1)

