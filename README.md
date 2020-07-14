# PyMacro
By picasso2005

- # What is it?
PyMacro is a macro handler written in python. It can have many sets of macro which are switched depending of the active window's title.

- # How can I add macros?
To add macro you need to create a python file in `/macros`. The name of this file must correspond with the name of the application linked to this set (exception for default which is loaded by default).
In this file, you will need to create a dictionary which will be named `hooks`. In this directory, put in the key, the hook assigned to the macro, and at the value a function object which will be the macro.

> Tip: create an empty list if you want to have no macros on a specific application

Example:
````python
def macro_a():
    print("Test macro a")  # Put your macro's script in this function


hooks = {
    "a": macro_a
}
````
This example will have a macro which will print `Test macro a` every time you will press `a`.
You have others exemples in `/macros`

- # What packages can I use to write my macros?
You can use every packages you want, but I recommend to use keyboard to simulate keyboard inputs or pyautogui (it can do keyboard input too but it can also do mouse events).
