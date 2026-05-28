"""
Recapture stories that failed in the first run (loading screens, wrong window, early pan frame).
Uses 4-second wait for more reliable loading before pausing.
Run: python redo_stories.py
"""
import subprocess
import time
import os
import re
import ctypes
import ctypes.wintypes as wintypes
from PIL import ImageGrab

STORY_SCREEN = (428, 138, 764, 703)
BASE_DIR = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\collections"

REDO = [
    ("2022", "Speed",             "https://www.instagram.com/stories/archive/17932063256711148/"),
    ("2022", "Cool",              "https://www.instagram.com/stories/archive/17991254743749168/"),
    ("2022", "Deep Sea",          "https://www.instagram.com/stories/archive/17964306662252050/"),
    ("2023", "Away",              "https://www.instagram.com/stories/archive/17993205533624395/"),
    ("2023", "Dog",               "https://www.instagram.com/stories/archive/18053760652572299/"),
    ("2023", "Lizard",            "https://www.instagram.com/stories/archive/17998632590438028/"),
    ("2023", "chameleon",         "https://www.instagram.com/stories/archive/18000509939041547/"),
    ("2023", "Pain",              "https://www.instagram.com/stories/archive/18074860252397051/"),
    ("2023", "age",               "https://www.instagram.com/stories/archive/18004064605999929/"),
    ("2023", "Rat-a-saur",        "https://www.instagram.com/stories/archive/18038122162523785/"),
    ("2024", "Dinosaur",          "https://www.instagram.com/stories/archive/18369015214098401/"),
    ("2024", "cat",               "https://www.instagram.com/stories/archive/18010004741281337/"),
    ("2024", "Over-weight",       "https://www.instagram.com/stories/archive/17893775718058876/"),
    ("2024", "Empty",             "https://www.instagram.com/stories/archive/18040423640085593/"),
    ("2024", "Crazy",             "https://www.instagram.com/stories/archive/18065741791609615/"),
    ("2025", "archer",            "https://www.instagram.com/stories/archive/18138890143444635/"),
    ("2025", "tenticles",         "https://www.instagram.com/stories/archive/17861425209575298/"),
    ("2025", "Be-calm",           "https://www.instagram.com/stories/archive/17973400130698552/"),
    ("2025", "horse",             "https://www.instagram.com/stories/archive/18106123996532680/"),
    ("2025", "Croc",              "https://www.instagram.com/stories/archive/17875000986260060/"),
    ("2025", "caw-caw",           "https://www.instagram.com/stories/archive/18051144887367787/"),
    ("2025", "Ra-sun",            "https://www.instagram.com/stories/archive/18174925420383960/"),
    ("2025", "Friend",            "https://www.instagram.com/stories/archive/17960184966059437/"),
    ("2025", "Guided-perspective","https://www.instagram.com/stories/archive/18079105319055753/"),
    ("2025", "Cat",               "https://www.instagram.com/stories/archive/18152549407429756/"),
    ("2025", "war-dog",           "https://www.instagram.com/stories/archive/18355619890237013/"),
    ("2025", "Hail-mary",         "https://www.instagram.com/stories/archive/18355619890237013/"),
    ("2025", "Prayer",            "https://www.instagram.com/stories/archive/18072046633763883/"),
]


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
    subprocess.Popen(f'start chrome "{url}"', shell=True)
    time.sleep(4)  # 4s — more loading time than original 2s run

    hwnd = focus_window("Instagram")
    if not hwnd:
        hwnd = focus_window("Chrome")
    if hwnd:
        time.sleep(0.3)
        send_space_key()
        time.sleep(0.3)

    img = ImageGrab.grab(bbox=STORY_SCREEN)
    img.save(output_path, "JPEG", quality=95)

    close_tab()

    return img.size


def main():
    total = len(REDO)
    print(f"Retrying {total} failed captures...\n")

    for i, (year, name, url) in enumerate(REDO):
        safe_name = clean_name(name)
        year_dir = os.path.join(BASE_DIR, year)
        os.makedirs(year_dir, exist_ok=True)
        output_path = os.path.join(year_dir, f"{safe_name}.jpg")

        print(f"[{i+1}/{total}] {year}/{safe_name} ...")
        try:
            size = capture_one(url, output_path)
            print(f"  -> Saved ({size[0]}x{size[1]}): {output_path}")
        except Exception as e:
            print(f"  -> ERROR: {e}")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
