import math

import pyautogui
import pynput
import pywinauto.mouse
import os
from mouse import listen
import time

patient_last_y = 1242
patient_first_y = 452
patient_last_x = 110


def roll():
    pass


def keyboard(*args, **kwargs):
    """读取鼠标当前所在位置"""
    capture_flag = pyautogui.alert(text='Please capture key coordinates.', title='Test')  # 提示关键点采集的弹窗
    if capture_flag:
        with pynput.mouse.Events() as event:
            for i in event:
                if isinstance(i, pynput.mouse.Events.Click):
                    print(i.x, i.y, i.button, i.pressed)
                    break  # 捕捉到一次关键点位置后，停止捕捉
    return i.x, i.y


a = listen([["q", keyboard, []], ["r", roll, []]], end_key='sss')
a.run()
patient_key_x = a.x_mouse
patient_key_y = a.y_mouse
n = math.floor((patient_key_y[2]- patient_key_y[1] - 140) / 126) + 1  # 鼠标滑轮滑动的次数
pywinauto.mouse.scroll((patient_key_x[1], patient_key_y[1]), -n)
patient_key_y2 = patient_key_y[2] - ((n - 1) * 126 + 140)
print(patient_key_y2)
# patient_export(patient_key_x, patient_key_y)
