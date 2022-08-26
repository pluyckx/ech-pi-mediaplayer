import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
print(f"mode: {GPIO.getmode()}")

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

states = {3: None, 5: None, 7: None}

def pin_changed(channel):
    global states
    
    state = GPIO.input(channel)
    if state != states[channel]:
        states[channel] = state
        print(f"pin{channel}: {states[channel]}")
    
GPIO.add_event_detect(3, GPIO.BOTH)
GPIO.add_event_detect(5, GPIO.BOTH)
GPIO.add_event_detect(7, GPIO.BOTH)

GPIO.add_event_callback(3, pin_changed)
GPIO.add_event_callback(5, pin_changed)
GPIO.add_event_callback(7, pin_changed)

while True:
    time.sleep(1)