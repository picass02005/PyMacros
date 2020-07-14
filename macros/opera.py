import keyboard
import pyperclip
import time
import requests
from urllib.parse import quote as query


def yt_search(search: str):
    r = requests.get(f"http://www.youtube.com/results?search_query={query(search)}")
    id_ = r.text.split("watch?v=")[1].split("\"")[0]
    title = r.text.split("title\":{\"runs\":[{\"text\":\"")[1].split("\"")[0]

    return {"url": f"https://youtube.com/watch?v={id_}", "title": title}


def F13():
    clipboard = pyperclip.paste()

    keyboard.send("ctrl+a")
    keyboard.send("ctrl+c")

    time.sleep(0.1)

    data = pyperclip.paste()

    pyperclip.copy(clipboard)

    keyboard.write(f"Searching {data} on youtube...")
    time.sleep(1)

    try:
        video = yt_search(data)
        keyboard.send("ctrl+a")
        keyboard.write(video['title'])
        time.sleep(3)
        keyboard.send("ctrl+a")
        keyboard.write(f"!sr {video['url']}")
    except KeyError:
        keyboard.send("ctrl+a")
        keyboard.write(f"Unable to research {data}")


hooks = {
    "F13": F13
}
