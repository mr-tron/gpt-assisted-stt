import time

from pynput.keyboard import Key, Listener
from audio import record_audio
from threading import Event, Thread
from ai import transcript, post_proccess
from xdo import Xdo


xdo = Xdo() # fake input for typing


def main():
    hotkey_manage = HotkeyManager()
    # Collect events until released
    with Listener(
            on_press=hotkey_manage.on_press,
            on_release=hotkey_manage.on_release) as listener:
        listener.join()

def text_processing(audio):
    text = transcript(audio)
    t = time.time()
    stream = post_proccess(text)
    print("get stream", stream)
    for chunk in stream:
        keyboard_type(chunk.choices[0].delta.content or "")
    print("printing %s" % (time.time() - t))


class HotkeyManager(object):
    def __init__(self):
        self.hotkey_state = 0
        self.stop = None

    def on_press(self, key):
        if key == Key.alt and self.hotkey_state == 0:
            self.hotkey_state = 1
        if key == Key.f8 and self.hotkey_state == 1:
            self.hotkey_state = 2
            self.stop = Event()
            Thread(target=record_audio, args=[self.stop, text_processing]).start()

    def on_release(self, key):
        if self.hotkey_state == 0:
            return
        if key == Key.f8 or key == Key.alt:
            self.hotkey_state = 0
            if self.stop is not None:
                self.stop.set()
                self.stop = None


def keyboard_type(text):
    window = xdo.get_focused_window()
    xdo.enter_text_window(window, text.encode('utf-8'), delay=6000)



if __name__ == '__main__':
    main()
