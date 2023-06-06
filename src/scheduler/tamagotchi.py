from PIL import Image
from picamera2 import Picamera2
import random
import time
import math
import os
import pickle

FILE = "tamagotchi"

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
        self.is_alive = True
        self.get_new_task()

    def get_new_task(self):
        task_kind = random.choice(TASKS)
        self.task = None
        if task_kind == "color":
            self.task = Task(task_kind, random.choice(list(COLORS.keys())))
        self.start_idle = -1
        return self.task

    def verify_task(self):
        if self.task is None:
            return "idle"
        if self.task.kind == "color":
            image = capture_image()
            closest_color = get_closest_color_to_image(image)
            print_closest_color_to_image(image)

            if closest_color == self.task.target:
                return "completed"
        if time.time() - self.task.start_time <= self.task_time:
            return "in progress"
        return "failed"

    def update(self):
        if self.is_alive:
            task_status = self.verify_task()
            if task_status == "idle" or task_status == "completed":
                if self.start_idle == -1:
                    self.start_idle = time.time()
                elif time.time() - self.start_idle >= self.idle_time:
                    self.get_new_task()
            if task_status == "failed":
                print("failed")
                #self.is_alive = False

    def get_task_text(self):
        if not self.is_alive:
            return "I'm dead"
        if self.task is None:
            return "Just chillin"
        else:
            if self.task.kind == "color":
                return "I want to see the color {0}, until {1} please :)".format(self.task.target, self.task.start_time + self.task_time)
        return ""


def tamagotchi_task():
    if os.path.exists(FILE):
        with open(FILE, 'rb') as tamagotchi_file:
            tamagotchi = pickle.load(tamagotchi_file)
    else:
        tamagotchi = Tamagotchi(30, 5)

    tamagotchi.update()
    print(tamagotchi.get_task_text())

    with open(FILE, 'wb+') as tamagotchi_file:
        pickle.dump(tamagotchi, tamagotchi_file)


if __name__ == "__main__":
    tamagotchi_task()
