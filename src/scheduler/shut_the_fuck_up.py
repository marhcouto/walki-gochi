import os
import pickle
import time
import RPi.GPIO as GPIO

TAMAGOTCHI_FILE = "tamagotchi"

BUZ = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZ, GPIO.OUT)

def beep_on():
    GPIO.output(BUZ, GPIO.HIGH)

def beep_off():
    GPIO.output(BUZ, GPIO.LOW)

def turn_leds_on():
    print("LEDs on")

def turn_leds_off():
    print("LEDs off")

beep_off()