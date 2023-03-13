import pyautogui
import pynput
import os
from mouse import listen


def keyboard(*args, **kwargs):
    """读取鼠标当前所在位置"""
    capture_flag = pyautogui.alert(text='Please capture key coordinates.', title='Test')  # 提示关键点采集的弹窗
    if capture_flag:
        with pynput.mouse.Events() as event:
            for i in event:
                if isinstance(i, pynput.mouse.Events.Click):
                    x_mouse = i.x
                    y_mouse = i.y
                    print(i.x, i.y, i.button, i.pressed)
                    break  # 捕捉到一次关键点位置后，停止捕捉
    return x_mouse, y_mouse


if __name__ == "__main__":
    screen_x, screen_y = pyautogui.size()  # 获取屏幕尺寸（分辨率×分辨率）
    global count  # 记录关键点采集的次数
    count = 0
    """"""
    a = listen([["qqq", keyboard, [], {}], ["awa", keyboard, [], {}]])
    a.run()
