"""
Automates capturing all Instagram story archive screenshots from stories.json.
Opens each URL in Chrome, pauses the story, captures the story frame, saves it.
Run: python run_all_stories.py
"""
import subprocess
import time
import json
import os
import re
import ctypes
import ctypes.wintypes as wintypes
from PIL import ImageGrab

STORY_SCREEN = (428, 138, 764, 703)
BASE_DIR = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\collections"
STORIES_JSON = r"C:\Users\user\Desktop\Gaurav\GuruDev\Support\stories.json"


def clean_name(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()


def focus_window(title_contains):
    user32 = ctypes.windll.user32
    found = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        buf = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, buf, 512)
        if title_contains in buf.value:
            found.append(hwnd)
            return False
        return True

    user32.EnumWindows(EnumWindowsProc(cb), 0)
    if found:
        hwnd = found[0]
        user32.ShowWindow(hwnd, 9)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        return hwnd
    return None


def send_key(vk):
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]
        _anonymous_ = ["_INPUT"]
        _fields_ = [("type", ctypes.c_ulong), ("_INPUT", _INPUT)]

    KEYEVENTF_KEYUP = 0x0002
    inputs = (INPUT * 2)(
        INPUT(type=1, ki=KEYBDINPUT(wVk=vk, dwFlags=0, wScan=0, time=0, dwExtraInfo=None)),
        INPUT(type=1, ki=KEYBDINPUT(wVk=vk, dwFlags=KEYEVENTF_KEYUP, wScan=0, time=0, dwExtraInfo=None)),
    )
    ctypes.windll.user32.SendInput(2, inputs, ctypes.sizeof(INPUT))


def send_space_key():
    send_key(0x20)  # VK_SPACE


def close_tab():
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]
        _anonymous_ = ["_INPUT"]
        _fields_ = [("type", ctypes.c_ulong), ("_INPUT", _INPUT)]

    KEYEVENTF_KEYUP = 0x0002
    VK_CONTROL = 0x11
    VK_W = 0x57
    inputs = (INPUT * 4)(
        INPUT(type=1, ki=KEYBDINPUT(wVk=VK_CONTROL, dwFlags=0, wScan=0, time=0, dwExtraInfo=None)),
        INPUT(type=1, ki=KEYBDINPUT(wVk=VK_W, dwFlags=0, wScan=0, time=0, dwExtraInfo=None)),
        INPUT(type=1, ki=KEYBDINPUT(wVk=VK_W, dwFlags=KEYEVENTF_KEYUP, wScan=0, time=0, dwExtraInfo=None)),
        INPUT(type=1, ki=KEYBDINPUT(wVk=VK_CONTROL, dwFlags=KEYEVENTF_KEYUP, wScan=0, time=0, dwExtraInfo=None)),
    )
    ctypes.windll.user32.SendInput(4, inputs, ctypes.sizeof(INPUT))


def capture_one(url, output_path):
    # Open URL in Chrome — Chrome comes to foreground automatically
    subprocess.Popen(f'start chrome "{url}"', shell=True)
    time.sleep(2)  # shorter wait — catch drawing early before video advances

    # Focus Chrome and pause the story
    hwnd = focus_window("Instagram")
    if not hwnd:
        hwnd = focus_window("Chrome")
    if hwnd:
        time.sleep(0.3)
        send_space_key()
        time.sleep(0.3)

    # Grab just the story frame region
    img = ImageGrab.grab(bbox=STORY_SCREEN)
    img.save(output_path, "JPEG", quality=95)

    close_tab()

    return img.size


def main():
    with open(STORIES_JSON, encoding="utf-8") as f:
        stories = json.load(f)

    all_items = [(yr, nm, url)
                 for yr, items in sorted(stories.items())
                 for nm, url in items.items()]
    total = len(all_items)
    done = 0

    print(f"Total stories: {total}\n")

    for year, name, url in all_items:
        safe_name = clean_name(name)
        year_dir = os.path.join(BASE_DIR, year)
        os.makedirs(year_dir, exist_ok=True)
        output_path = os.path.join(year_dir, f"{safe_name}.jpg")

        print(f"[{done+1}/{total}] Capturing {year}/{safe_name} ...")
        try:
            size = capture_one(url, output_path)
            print(f"  -> Saved ({size[0]}x{size[1]}): {output_path}")
        except Exception as e:
            print(f"  -> ERROR: {e}")

        done += 1

    print(f"\nFinished: {done} captured.")


if __name__ == "__main__":
    main()
