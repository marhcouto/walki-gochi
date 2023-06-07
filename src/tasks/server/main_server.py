#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get, post, run, route, request, template, static_file
from server.PCA9685 import PCA9685
import socket
import os
import subprocess
import pickle

TAMAGOTCHI_FILE = "tamagotchi"
SENSORS_FILE = "can_move_forward.pkl"

# Set servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0  # Sets the initial step length
VPulse = 1500  # Sets the initial Pulse
VStep = 0  # Sets the initial step length
front = None
side = None
tamagotchi = None


@get("/")
def index():
    return template(os.path.dirname(os.path.abspath(__file__)) + "/server/index")


@get("/state")
def state():
    global tamagotchi
    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/" + TAMAGOTCHI_FILE):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + TAMAGOTCHI_FILE, 'rb') as tamagotchi_file:
            tamagotchi = pickle.load(tamagotchi_file)
        return tamagotchi.get_text()
    else:
        return ""


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root=os.path.dirname(os.path.abspath(__file__)) + "/server")


@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root=os.path.dirname(os.path.abspath(__file__)) + "/server/fonts")


@post("/cmd")
def cmd():
    global HStep, VStep, front, side
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    print(code)

    if code[:4] == "stop":
        if (len(code) > 4):
            if (code[4:] == "forward"):
                front = None
            elif (code[4:] == "left"):
                side = None
            elif (code[4:] == "camera"):
                HStep = 0
                VStep = 0
        else:
            front = None
            side = None
            HStep = 0
            VStep = 0

    elif code == "forward":
        front = True
    elif code == "backward":
        front = False
    elif code == "turnleft":
        side = False
    elif code == "turnright":
        side = True
    elif code == "up":
        VStep = -50
        print("up")
    elif code == "down":
        VStep = 50
        print("down")
    elif code == "left":
        HStep = 100
        print("left")
    elif code == "right":
        HStep = -100
        print("right")

    # Sensors
    # can_move_forward = True
    # if os.path.exists(SENSORS_FILE):
    #     with open(SENSORS_FILE, 'rb') as f:
    #         can_move_forward = pickle.load(f)
    # if not can_move_forward and front:
    #     front = None

    intention = ""
    if side == True:
        intention = "right"
    elif side == False:
        intention = "left"
    else:
        if front == True:
            intention = "forward"
        elif front == False:
            intention = "backward"
        else:
            intention = "stop"

    # Save movement intention
    with open("input.pkl", "wb+") as f:
        pickle.dump({"intention": intention, "speed": speed, "HStep": HStep, "VStep": VStep}, f)

    return "OK"

def start():
    lastpath = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(['python3', lastpath + "/mjpeg_server.py"])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    localhost = s.getsockname()[0]
    run(host=localhost, port=3000)


if (__name__ == "__main__"):
    start()
