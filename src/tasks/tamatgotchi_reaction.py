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


def main():
    tamagotchi = None
    if os.path.exists(TAMAGOTCHI_FILE):
        with open(TAMAGOTCHI_FILE, 'rb') as tamagotchi_file:
            tamagotchi = pickle.load(tamagotchi_file)

    if tamagotchi is not None:
        if tamagotchi.state == "sad":
            beep_on()
        elif tamagotchi.state == "happy":
            deltatime = time.time() - tamagotchi.state_time
            if deltatime >= tamagotchi.reaction_time / 3.0 and deltatime <= 2 * tamagotchi.reaction_time / 3.0:
                beep_off()
            else:
                beep_on()
        elif tamagotchi.state == "idle":
            beep_off()


if __name__ == "__main__":
    main()
