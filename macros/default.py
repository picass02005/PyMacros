import time

from threading import Thread
import win32api
import win32con
from config import *

is_active = False


class thread_click(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global is_active

        if win32api.GetKeyState(0x01) + 2 > 0:
            key = [win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP]

        elif win32api.GetKeyState(0x02) + 2 > 0:
            key = [win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP]

        else:
            key = None

        if key is not None:
            is_active = True
            while is_active:
                x, y = win32api.GetCursorPos()
                win32api.mouse_event(key[0], x, y, 0, 0)
                time.sleep(CLICK_SLEEP / 2)
                win32api.mouse_event(key[1], x, y, 0, 0)
                time.sleep(CLICK_SLEEP / 2)


def F13():
    global is_active

    if is_active:
        is_active = False

    else:
        thread_click().start()

    time.sleep(0.1)


hooks = {
    "F13": F13
}
