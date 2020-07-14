import keyboard


def F13():
    keyboard.write("CECI EST UN TEST D'ECRITURE DANS DISCORD", delay=0.03)


hooks = {
    "F13": F13
}
