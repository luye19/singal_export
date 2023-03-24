import math
import pyautogui
import pynput
import pywinauto.mouse
from mouse import listen
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--Mouse_time', type=float, default=0.2, help='鼠标到达指定位置所用时间（second）')
parser.add_argument('-Intervals_num', type=int, default=34, help='第一个病人与最后一个病人之间的间隔数量')
# parser.add_argument('--Patient_num', type=int, default=80, help='导出的病人总数')
parser.add_argument('--Wait_time', type=int, default=1, help='数据正在导出的等待时间（second）')
args = parser.parse_args()


def keyboard():
    """读取鼠标当前所在位置"""
    flag = pyautogui.alert(text='Please capture key coordinates.', title='singal export')  # 提示关键点采集的弹窗
    if flag:
        with pynput.mouse.Events() as event:
            for i in event:
                if isinstance(i, pynput.mouse.Events.Click):
                    print(i.x, i.y, i.button, i.pressed)
                    break  # 捕捉到一次关键点位置后，停止捕捉
    return i.x, i.y


def roll():
    """捕捉滑轮滚动一个单位的距离"""
    flag = pyautogui.alert(text='Measure the distance of mouse scrolling', title='singal export')  # 提示关键点采集的弹窗

    if flag:
        with pynput.mouse.Events() as event:
            for i in event:
                if isinstance(i, pynput.mouse.Events.Click):
                    first_x = i.x
                    first_y = i.y
                    print(i.x, i.y, i.button, i.pressed)
                    break
    # pyautogui.scroll(600)
    pyautogui.mouseUp()
    pywinauto.mouse.scroll((first_x, first_y), -args.Roll_num)  # 滑轮向上滚动
    time.sleep(1)
    with pynput.mouse.Events() as event:
        for i in event:
            if isinstance(i, pynput.mouse.Events.Click):
                sec_x = i.x
                sec_y = i.y
                print(i.x, i.y, i.button, i.pressed)
                break
    return (first_x - sec_x) / args.Roll_num, (first_y - sec_y) / args.Roll_num


def mouse_click(x, y):
    pyautogui.moveTo(x, y, duration=args.Mouse_time)  # 鼠标移动到指定位置
    pyautogui.click(button='left')  # 在当前位置点击左键


def patient_export(key_x, key_y):
    """一个患者数据导出的完整流程"""
    for i in key_x.keys():
        mouse_click(key_x[i], key_y[i])
        if i == 6:
            mouse_click(key_x[i], key_y[i])
            time.sleep(args.Wait_time)


if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # 启用自动防故障功能，左上角的坐标为（0，0），将鼠标移到屏幕的左上角，来抛出failSafeException异常
    capture_flag = pyautogui.alert(text="Press 'c' to capture the coordinates of the key points.\rPress 'r' to "
                                        "measure the distance scrolled by the scroll wheel.\rPress 's' to start "
                                        "automatic data export.", title='singal export')  # 提示关键点采集的弹窗

    Patient_num = int(pyautogui.prompt('请输入要导出的患者总数：'))

    """捕捉关键点坐标"""
    a = listen([["c", keyboard, []], ["r", roll, []]], end_key='s')
    a.run()
    a.x_mouse.popitem()
    a.y_mouse.popitem()
    tech_names = {1, 2, 3, 4, 5, 6, 7}
    patient_key_x = {key: value for key, value in a.x_mouse.items() if key in tech_names}
    patient_key_y = {key: value for key, value in a.y_mouse.items() if key in tech_names}
    patient_first_x = a.x_mouse[2]
    patient_first_y = a.y_mouse[2]
    patient_last_x = a.x_mouse[8]
    patient_last_y = a.y_mouse[8]
    patient_y = (patient_last_y - patient_first_y) / args.Intervals_num

    for i in range(args.Intervals_num):
        if patient_key_y[2] <= patient_last_y:
            patient_export(patient_key_x, patient_key_y)
            patient_key_y[2] = patient_key_y[2] + patient_y  # 将第一页的数据导出

    patient_key_y[2] = patient_last_y

    for j in range(Patient_num - args.Intervals_num -1):
        mouse_click(patient_last_x, patient_last_y)
        pyautogui.press('down')
        patient_export(patient_key_x, patient_key_y)
    txt = f'Export {Patient_num} patient data'
    pyautogui.alert(text=txt, title='singal export')  # 提示关键点采集的弹窗

