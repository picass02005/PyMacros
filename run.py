import ctypes
import importlib
import os
import time
from ctypes import wintypes
from threading import Thread

import keyboard
import psutil
import pystray
from PIL import Image
from pystray import MenuItem as item

from config import *

# ================================= Set the program priority below normal if possible ==================================
try:
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

except:
    pass
# ======================================================================================================================

activated = True

hotkeys = {}


def get_active_window_process():
    user32 = ctypes.windll.user32

    h_wnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))

    try:
        return psutil.Process(pid=pid.value)
    except psutil.AccessDenied:
        return None


def load_hooks(name: str):
    global hotkeys

    hooks_name = "default"
    for i in os.listdir("macros"):
        i = i.split(".py")[0]
        if i.lower() in name.lower():
            hooks_name = i

    print(f"Load hooks referenced in {hooks_name} (window name: {name})")
    hooks = importlib.import_module(f"macros.{hooks_name}")
    importlib.reload(hooks)

    hotkeys = hooks.hooks


def press(key):
    global hotkeys

    for i in hotkeys.items():
        tmp = True
        for j in i[0].lower().split("+"):
            if not keyboard.is_pressed(j.strip()):
                tmp = False

        if tmp:
            i[1]()


class main_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.daemon = True

        self.window = None

    def run(self):
        global activated
        global icon
        global hotkeys

        while True:
            if not activated:
                self.window = None
                hotkeys = {}
                time.sleep(ACTUALISATION_TIME_DISABLED)

            else:
                if self.window != get_active_window_process():
                    self.window = get_active_window_process()
                    load_hooks(self.window.name())

                time.sleep(ACTUALISATION_TIME_WINDOW)


def toggle_activated():
    global activated
    global icon

    if activated:
        activated = False
        icon.icon = Image.open("images/tray_disabled.png")
        icon.menu = pystray.Menu(item('PyMacro', lambda: None, enabled=False),
                                 item('Enable', lambda: toggle_activated()),
                                 item('Exit', lambda: icon.stop()))

        print("SCRIPT DISABLED")

    else:
        activated = True
        icon.icon = Image.open("images/tray_enabled.png")
        icon.menu = pystray.Menu(item('PyMacro', lambda: None, enabled=False),
                                 item('Disable', lambda: toggle_activated()),
                                 item('Exit', lambda: icon.stop()))

        print("SCRIPT ENABLED")


keyboard.on_press(press)

image = Image.open("images/tray_enabled.png")
menu = pystray.Menu(item('PyMacro', lambda: None, enabled=False),
                    item('Disable', lambda: toggle_activated()),
                    item('Exit', lambda: icon.stop()))
icon = pystray.Icon("PyMacro", image, "PyMacro - By picasso2005", menu)

main_thread().start()

icon.run()
