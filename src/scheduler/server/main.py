#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get, post, run, route, request, template, static_file
from .AlphaBot import AlphaBot
from .PCA9685 import PCA9685
import threading
import socket  # ip
import os
import subprocess

Ab = AlphaBot()
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Set servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0  # Sets the initial step length
VPulse = 1500  # Sets the initial Pulse
VStep = 0  # Sets the initial step length
front = None
side = None

pwm.setServoPulse(1, VPulse)
pwm.setServoPulse(0, HPulse)


@get("/")
def index():
    return template(os.path.dirname(os.path.abspath(__file__)) + "/index")


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root=os.path.dirname(os.path.abspath(__file__)))


@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root=os.path.dirname(os.path.abspath(__file__)) + "/fonts")


@post("/cmd")
def cmd():
    global HStep, VStep, front, side
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    print(code)
    if (speed != None):
        Ab.setPWMA(float(speed))
        Ab.setPWMB(float(speed))
        print(speed)
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
        print("stop")

    elif code == "forward":
        front = True
        print("forward")
    elif code == "backward":
        front = False
        print("backward")
    elif code == "turnleft":
        side = False
        print("turnleft")
    elif code == "turnright":
        side = True
        print("turnright")
    elif code == "up":
        VStep = -20
        print("up")
    elif code == "down":
        VStep = 20
        print("down")
    elif code == "left":
        HStep = 20
        print("left")
    elif code == "right":
        HStep = -20
        print("right")

    if side == True:
        Ab.right()
    elif side == False:
        Ab.left()
    else:
        if front == True:
            Ab.forward()
        elif front == False:
            Ab.backward()
        else:
            Ab.stop()
    return "OK"


def timerfunc():
    global HPulse, VPulse, HStep, VStep, pwm

    if (HStep != 0):
        HPulse += HStep
        if (HPulse >= 2500):
            HPulse = 2500
        if (HPulse <= 500):
            HPulse = 500
        # set channel 2, the Horizontal servo
        pwm.setServoPulse(0, HPulse)

    if (VStep != 0):
        VPulse += VStep
        if (VPulse >= 2500):
            VPulse = 2500
        if (VPulse <= 500):
            VPulse = 500
        # set channel 3, the vertical servo
        pwm.setServoPulse(1, VPulse)

    global t  # Notice: use global variable!
    t = threading.Timer(0.02, timerfunc)
    t.start()


def camera():
    lastpath = os.path.abspath(os.path.join(os.getcwd(), "../"))
    print("lastpath = %s" % lastpath)
    subprocess.Popen(['python3', lastpath + "mjpeg_server.py"])
    # campath = lastpath + '/mjpg-streamer/mjpg-streamer-experimental/'
    # print("campath = %s" %campath)
    # os.system(campath  + './mjpg_streamer -i "' + campath + './input_uvc.so" -o "' + campath + './output_http.so -w ' + campath + './www"')

# tcamera = threading.Thread(target = camera)
# tcamera.setDaemon(True)
# tcamera.start()
# tcamera = threading.Thread(target = camera)
# tcamera.setDaemon(True)
# tcamera.start()


def start():
    lastpath = os.path.dirname(os.path.abspath(__file__))
    print("lastpath = %s" % lastpath)
    subprocess.Popen(['python3', lastpath + "/../mjpeg_server.py"])

    t = threading.Timer(0.02, timerfunc)
    t.setDaemon(True)
    t.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    localhost = s.getsockname()[0]
    run(host=localhost, port=3000)


if (__name__ == "__main__"):
    start()
