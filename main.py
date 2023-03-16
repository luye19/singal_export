import math

import pyautogui
import pynput
import pywinauto.mouse
import os
from mouse import listen
import time


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


def roll():
    """捕捉滑轮滚动一个单位的距离"""
    capture_flag = pyautogui.alert(text='Please capture key coordinates.', title='Test')  # 提示关键点采集的弹窗
    if capture_flag:
        with pynput.mouse.Events() as event:
            for i in event:
                if isinstance(i, pynput.mouse.Events.Click):
                    first_x = i.x
                    first_y = i.y
                    print(i.x, i.y, i.button, i.pressed)
                    break
    # pyautogui.scroll(600)
    n = 5
    pywinauto.mouse.scroll((first_x, first_y), -n)  # 滑轮向上滚动
    time.sleep(3)
    with pynput.mouse.Events() as event:
        for i in event:
            if isinstance(i, pynput.mouse.Events.Click):
                sec_x = i.x
                sec_y = i.y
                print(i.x, i.y, i.button, i.pressed)
                break
    return (first_x - sec_x)/n, (first_y - sec_y)/n


def mouse_click(x, y):
    pyautogui.moveTo(x, y, duration=0.2)  # 鼠标移动到指定位置
    pyautogui.click(button='left')  # 在当前位置点击左键


def patient_export(key_x, key_y):
    """一个患者数据导出的完整流程"""
    for i in key_x.keys():
        mouse_click(key_x[i], key_y[i])
        if i == 6:
            mouse_click(key_x[i], key_y[i])
            time.sleep(1)


if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
    screen_x, screen_y = pyautogui.size()  # 获取屏幕尺寸（分辨率×分辨率）
    """捕捉关键点坐标"""
    a = listen([["q", keyboard, []], ["r", roll, []]], end_key='sss')
    a.run()
    a.x_mouse.popitem()
    a.y_mouse.popitem()
    tech_names = {1, 2, 3, 4, 5, 6, 7}
    patient_key_x = {key: value for key, value in a.x_mouse.items() if key in tech_names}
    patient_key_y = {key: value for key, value in a.y_mouse.items() if key in tech_names}
    patient_first_x = a.x_mouse[2]
    patient_first_y = a.y_mouse[2]
    patient_sec_x = a.x_mouse[8]
    patient_sec_y = a.y_mouse[8]
    patient_last_x = a.x_mouse[9]
    patient_last_y = a.y_mouse[9]
    patient_y = patient_sec_y - patient_first_y  # 截图一个患者框，通过图片的像素值来确定
    roll_y = a.y_mouse[10]
    for i in range(80):
        patient_key_y[2] = patient_key_y[2] + patient_y
        if patient_key_y[2] > patient_last_y:
            n = math.floor((patient_last_y - patient_first_y - 110) / 110) + 1  # 鼠标滑轮滑动的次数
            pywinauto.mouse.scroll((patient_last_x, patient_last_y), -n) #负数，滑轮向下滚动
            time.sleep(3)
            patient_key_y[2] = patient_key_y[2] - ((n - 1) * 110 + 110)
            print("滑动：", patient_key_y[2])
            patient_export(patient_key_x, patient_key_y)
        else:
            patient_export(patient_key_x, patient_key_y)
