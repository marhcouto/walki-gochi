import RPi.GPIO as GPIO
from server.AlphaBot import AlphaBot
import pickle
import os

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

Ab = AlphaBot()

INPUT_FILE = 'input.pkl'


def main():
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    can_move = not ((DL_status == 0) or (DR_status == 0))

    input = None
    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/" + INPUT_FILE):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + INPUT_FILE, 'rb') as f:
            input = pickle.load(f)

    if input is None:
        return

    if (input["speed"] != None):
        Ab.setPWMA(float(input["speed"]))
        Ab.setPWMB(float(input["speed"]))

    if not can_move:
        Ab.stop()

    if input["intention"] == "forward" and can_move:
        Ab.forward()
    elif input["intention"] == "backward":
        Ab.backward()
    elif input["intention"] == "left":
        Ab.left()
    elif input["intention"] == "right":
        Ab.right()
    elif input["intention"] == "stop":
        Ab.stop()

    # print("START AVOIDANCE")
    # DR_status = GPIO.input(DR)
    # DL_status = GPIO.input(DL)
    # can_move = not ((DL_status == 0) or (DR_status == 0))
    # print("Can move: ", can_move)

    # with open('can_move_forward.pkl', 'wb') as f:
    #     pickle.dump(can_move, f)

    # print("DONE AVOIDANCE")


# try:
#     while True:
#         DR_status = GPIO.input(DR)
#         DL_status = GPIO.input(DL)
# #        print(DR_status,DL_status)
#         if((DL_status == 0) or (DR_status == 0)):
#             Ab.left()
#             #Ab.right()
#             time.sleep(0.002)
#             Ab.stop()
#         #    print("object")
#         else:
#             Ab.forward()
#         #    print("forward")

# except KeyboardInterrupt:
#     GPIO.cleanup();
