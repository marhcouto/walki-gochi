import os
import pickle

from server.PCA9685 import PCA9685


pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# Set servo parameters
HPulse = 1500  # Sets the initial Pulse
HStep = 0  # Sets the initial step length
VPulse = 1500  # Sets the initial Pulse
VStep = 0  # Sets the initial step length

pwm.setServoPulse(1, VPulse)
pwm.setServoPulse(0, HPulse)

INPUT_FILE = 'input.pkl'
CAM_MOVEMENT_FILE = 'cam_movement.pkl'


def main():
    input = None
    cam_movement = None

    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/" + INPUT_FILE):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + INPUT_FILE, 'rb') as f:
            input = pickle.load(f)

    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/" + CAM_MOVEMENT_FILE):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + CAM_MOVEMENT_FILE, 'rb') as f:
            cam_movement = pickle.load(f)

    HPulse = 500
    VPulse = 500
    if cam_movement is not None:
        HPulse = cam_movement["HPulse"]
        VPulse = cam_movement["VPulse"]

    HStep = 0
    VStep = 0
    if input is not None:
        HStep = input["HStep"]
        VStep = input["VStep"]

    if (HStep != 0):
        HPulse += HStep
        if (HPulse >= 2500):
            HPulse = 2500
        if (HPulse <= 500):
            HPulse = 500
        # set channel 0, the Horizontal servo
    pwm.setServoPulse(0, HPulse)

    if (VStep != 0):
        VPulse += VStep
        if (VPulse >= 2500):
            VPulse = 2500
        if (VPulse <= 500):
            VPulse = 500
        # set channel 1, the vertical servo
    pwm.setServoPulse(1, VPulse)

    # Save movement parameters
    with open(os.path.dirname(os.path.abspath(__file__)) + "/" + CAM_MOVEMENT_FILE, "wb+") as f:
        pickle.dump({"HPulse": HPulse, "VPulse": VPulse}, f)
