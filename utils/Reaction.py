import numpy as np
import time

import pyautogui
from PIL import ImageChops, ImageGrab


def surprise_attack(allow_surprise, stage, opmove, grab_area=(1120, 800, 1200, 860)):
    '''
    If my army is near the enemy's base, choose cavalry to surprise them.
    '''
    if allow_surprise:
        img = ImageGrab.grab(grab_area)
        pixels = img.load()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                if pixels[x, y][0] >= 160:  # 我的兵是红色的，只要有一个杀入禁区我就派兵。如果对方出Lord，我就出High Lord。否则我出骑兵。

                    if stage == 0:
                        if opmove >= 14 or opmove == 12:  # 对付Lord，Iron Knight和Immortal用Monk。
                            return 9
                        else:
                            return 11
                    else:
                        return 11

    return False


def defense(grab_area=(720, 800, 930, 860)):
    '''
    If the enemy is near my base, choose High Lord to defense.
    '''
    img = ImageGrab.grab(grab_area)
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            if pixels[x, y][2] >= 160:  # 对方的兵是蓝色的，只要有一个杀入禁区我就用High Lord防御。
                return True

    return False


def detect_diff(grab_area=(1000, 880, 1600, 1030)):  # 左上点和右下点的坐标
    '''
    Detect the shining part in the game UI, aka the opponet's choice.
    '''
    image_one = ImageGrab.grab(grab_area)
    time.sleep(0.01)
    image_two = ImageGrab.grab(grab_area)
    diff = ImageChops.difference(image_one, image_two)
    return diff


# 标识出横坐标的范围，以便确定对方兵种
# X coordinates of the areas of your opponent's soldiers (the blue army).
pos_map = {(22, 90): 1,
           (90, 158): 2,
           (158, 226): 3,
           (226, 294): 4,
           (294, 362): 5,
           (362, 430): 6,
           (430, 498): 7,
           (498, 566): 8}


class CustomError(Exception):
    def __init__(self, ErrorInfo):
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


def get_opponent_move(pos_map=pos_map):
    '''
    Get the opponent's army.
    '''
    cut = detect_diff()
    pixels = cut.load()
    width, height = cut.size
    x_all = []
    y_all = []
    for x in range(width):
        for y in range(height):
            if pixels[x, y][0] > 1:   # 找到变化框框的颜色，黄色且变化较为剧烈，则RGB红色几乎一定大于1
                x_all.append(x)
                y_all.append(y)

    # 最初的频闪会出现两处不同，此时不同的数据点较多，本次结果应当忽略
    if len(x_all) > 8500:
        raise CustomError('Ignored!')

    x_mean = np.mean(x_all)
    y_mean = np.mean(y_all)

    # 纵坐标以76为界
    # Y coordinates of the opponent's soldier is distinguished by 76. 
    if y_mean < 76:
        prefix = 0
    else:
        prefix = 8

    for i in pos_map.keys():
        if x_mean > i[0] and x_mean < i[1]:
            suffix = pos_map[i]
            break

    move = prefix + suffix

    return move

# Coordinates of the areas of your soldier (the red army).
area_map = {1: (395, 923),
            2: (461, 923),
            3: (527, 923),
            4: (593, 923),
            5: (659, 923),
            6: (725, 923),
            7: (791, 923),
            8: (857, 923),
            9: (395, 994),
            10: (461, 994),
            11: (527, 994),
            12: (593, 994),
            13: (659, 994),
            14: (725, 994),
            15: (791, 994),
            16: (857, 994)
            }


# Quicker clicks!
pyautogui.PAUSE = 0.01


def click_area(my_move, area_map=area_map):
    '''
    Clicking to choose my army.
    '''
    x, y = area_map[my_move]
    pyautogui.click(x, y, clicks=1, interval=0.0, button='left', duration=0.0)
