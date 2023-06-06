from PIL import Image
from picamera2 import Picamera2
from io import BytesIO
import random
import time
import math
import os
import pickle

TAMAGOTCHI_FILE = "tamagotchi"
CAPTURE_FILE = "captures"

COLORS = {"red": (255, 0, 0),
          "brown": (150, 75, 0),
          "orange": (255, 127, 0),
          "yellow": (255, 255, 0),
          "green": (0, 255, 0),
          "cyan": (0, 255, 255),
          "blue": (0, 0, 255),
          "purple": (127, 0, 255),
          "pink": (255, 0, 127),
          "black": (0, 0, 0),
          }

TASKS = ["color"]

def require_sequence(images, target_color, target_sequence=5):
    counter = 0
    for image in images:
        closest_color = get_closest_color(get_dominant_color(image))
        if closest_color == target_color:
            counter += 1
            if counter >= target_sequence:
                return True
        else:
            counter = 0
    return False

def get_direct_color_dif(color1, color2):
    return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2])

def get_weighted_color_dif(color1, color2):
    delta_r = abs(color1[0] - color2[0])
    delta_g = abs(color1[1] - color2[1])
    delta_b = abs(color1[2] - color2[2])
    red_mean = (color1[0] + color2[0]) / 2.0
    if red_mean < 128:
        return math.sqrt(2 * delta_r ** 2 + 4 * delta_g ** 2 + 3 * delta_b ** 2)
    return math.sqrt(3 * delta_r ** 2 + 4 * delta_g ** 2 + 2 * delta_b ** 2)

def get_closest_color(color):
    min_dif = 1000
    current_color = "white"
    for key in COLORS:
        dif = get_weighted_color_dif(color, COLORS[key])
        if dif < min_dif:
            current_color = key
            min_dif = dif
    return current_color


def get_closest_color_to_image(pil_img):
    dominant_color = get_dominant_color(pil_img)
    return get_closest_color(dominant_color)


def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

def capture_image():
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.start()
    np_array = picam2.capture_array()
    picam2.stop()

    return Image.fromarray(np_array)

def load_images():
    if os.path.exists(CAPTURE_FILE):
        with open(CAPTURE_FILE, 'rb') as capture_file:
            image_list = pickle.load(capture_file)

    pil_image_list = []
    for image_bytes in image_list:
        #pil_image_list.append(Image.frombytes('RGBA', (640, 480), image_bytes, 'raw'))
        stream = BytesIO(image_bytes)
        pil_image_list.append(Image.open(stream).convert("RGBA"))
    return pil_image_list

def print_current_color():
    print_closest_color_to_image(capture_image())


def print_closest_color_to_image(pil_img):
    print("I'm currently seeing {0} which is closest to {1}".format(
        get_dominant_color(pil_img), get_closest_color_to_image(pil_img)))


class Task:
    def __init__(self, kind, target=None):
        self.kind = kind
        self.start_time = time.time()
        self.target = target


class Tamagotchi:
    def __init__(self, task_time, idle_time):
        self.task_time = task_time
        self.idle_time = idle_time
        self.reaction_time = self.idle_time / 2
        self.state = "idle"
        self.state_time = time.time()
        self.current_color = (0, 0, 0, 0)
        self.get_new_task()

    def get_new_task(self):
        task_kind = random.choice(TASKS)
        self.task = None
        if task_kind == "color":
            self.task = Task(task_kind, random.choice(list(COLORS.keys())))
        self.start_idle = -1
        self.state = "in progress"
        self.state_time = time.time()
        return self.task

    def verify_task(self):
        if self.state == "in progress":
            if self.task.kind == "color":
                images = load_images()
                last_image = images[0]
                self.current_color = get_dominant_color(last_image)
                if require_sequence(images, self.task.target, 2):
                    self.state = "completed"
                    self.state_time = time.time()
            if time.time() - self.task.start_time > self.task_time:
                self.state = "failed"
                self.state_time = time.time()

    def update(self):
        if self.state == "in progress":
            self.verify_task()
        else:
            if self.start_idle == -1:
                self.start_idle = time.time()
            elif time.time() - self.start_idle >= self.idle_time:
                self.get_new_task()

    def get_text(self):
        if self.state == "in progress" and self.task.kind == "color":
            return "I want to see the color {0}, until {1} please. Currently I'm seeing {2} which is closest to {3}".format(self.task.target, self.task.start_time + self.task_time, self.current_color, get_closest_color(self.current_color))
        elif self.state == "completed":
            return "Request fulfilled!!!"
        elif self.state == "failed":
            return "Request failed..."
        elif self.state == "happy":
            return "I'm so happy right now!!! :)"
        elif self.state == "sad":
            return "I'm so sad right now ;("
        else:
            return "Just chillin"


def tamagotchi_task():
    if os.path.exists(TAMAGOTCHI_FILE):
        with open(TAMAGOTCHI_FILE, 'rb') as tamagotchi_file:
            tamagotchi = pickle.load(tamagotchi_file)
    else:
        tamagotchi = Tamagotchi(30, 5)

    tamagotchi.update()
    print(tamagotchi.get_text())

    with open(TAMAGOTCHI_FILE, 'wb+') as tamagotchi_file:
        pickle.dump(tamagotchi, tamagotchi_file)


if __name__ == "__main__":
    tamagotchi_task()
