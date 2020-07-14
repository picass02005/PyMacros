"""
This is a example macro set which will be used when discord is the active window
"""

import keyboard


def macro_a():
    keyboard.send("This message is written every times you press A")


def macro_b():
    keyboard.send("You pressed B!")


hooks = {
    "A": macro_a,
    "B": macro_b
}
