import pyautogui
import pynput
import os
from pynput.keyboard import Listener
import time

"""鼠标监视，读取关键点坐标"""
# with pynput.mouse.Events() as event:
#     for i in event:
#         # 迭代用法。
#         if isinstance(i, pynput.mouse.Events.Move):
#             # 鼠标移动事件。
#             print(i.x, i.y)
#             # 不要直接打印`i`，模块这里有问题，会报错。
#
#         elif isinstance(i, pynput.mouse.Events.Click):
#             # 鼠标点击事件。
#             print(i.x, i.y, i.button, i.pressed)
#             # 这个i.button就是上文所说的“鼠标按键”中的一个，用is语句判断即可。
#
#         elif isinstance(i, pynput.mouse.Events.Scroll):
#             # 鼠标滚轮。
#             print(i.x, i.y, i.dx, i.dy)


class listen:
    """对特定按键做出响应"""
    def __init__(self, listen_lst, time_min=0.5, str_len=30, end_key="ppppp"):
        # listen_lst:["qqqq",func,args,kwargs],按下qqqq后调用函数func(*args,**kwargs)
        # time.min代表按键最短间隔，超过时间则按键清零
        # str_len 最长监听长度
        self.listen_lst = sorted(listen_lst, key=lambda x: len(x[0]))  # 按照"qqqq"长度排序
        self.listen_lst.append([end_key, self.stop_listen, [], {}])
        self.time_min = time_min
        self.now_str = ""
        self.str_len = str_len
        self.now_time = time.time()
        self.listener = None

    def on_press(self, key):
        key = str(key).replace("'", "")
        mid_time = time.time()
        if mid_time > self.now_time + self.time_min:
            self.now_str = key
        else:
            self.now_str = self.now_str + key
        self.now_time = mid_time
        if len(self.now_str) > self.str_len:
            self.now_str = self.now_str[-self.str_len:]
        for item in self.listen_lst:
            listen_key = item[0]
            now_str = self.now_str[-len(listen_key):]
            if (listen_key == now_str):
                print("按下", now_str)
                item[1](*item[2], **item[3])

    def stop_listen(self):
        if self.listener is not None:
            self.listener.stop()

    def run(self):
        with Listener(on_press=self.on_press) as listener:
            self.listener = listener
            listener.join()


# if __name__ == '__main__':
#     def test(*args, **kwargs):
#         print("test", args, kwargs)
#
#
#     a = listen([["qqq", test, (1, 2, 3), {"1": 2}], ["awa", test, [], {}]])
#     a.run()
