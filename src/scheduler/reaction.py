import os
import pickle
import time
from tamagotchi.py import Tamagotchi
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2

TAMAGOTCHI_FILE = "tamagotchi"

BUZ = 4
GPIO.setup(BUZ, GPIO.OUT)

def beep_on():
    GPIO.output(BUZ, GPIO.HIGH)

def beep_off():
    GPIO.output(BUZ, GPIO.LOW)

def turn_leds_on():
    print("LEDs on")

def turn_leds_off():
    print("LEDs off")

def reaction_task():
    if os.path.exists(TAMAGOTCHI_FILE):
        with open(TAMAGOTCHI_FILE, 'rb') as tamagotchi_file:
            tamagotchi = pickle.load(tamagotchi_file)

    if tamagotchi:
        if tamagotchi.state == "failed":
            beep_on()
            tamagotchi.state = "sad"
            tamagotchi.state_time = time.time()
        elif tamagotchi.state == "sad" and time.time() - tamagotchi.state_time >= tamagotchi.reaction_time:
            beep_off()
            tamagotchi.state = "idle"
            tamagotchi.state_time = time.time()
        elif tamagotchi.state == "completed":
            turn_leds_on()
            tamagotchi.state = "happy"
            tamagotchi.state_time = time.time()
        elif tamagotchi.state == "happy" and time.time() - tamagotchi.state_time >= tamagotchi.reaction_time:
            turn_leds_off()
            tamagotchi.state = "idle"
            tamagotchi.state_time = time.time()

        with open(TAMAGOTCHI_FILE, 'wb+') as tamagotchi_file:
            pickle.dump(tamagotchi, tamagotchi_file)


if __name__ == "__main__":
    reaction_task()