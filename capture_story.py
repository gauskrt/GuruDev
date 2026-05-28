"""
Capture a story frame from the currently open Instagram story in Chrome.
Usage: python capture_story.py <output_path>

Absolute screen coordinates of the Instagram story frame when Chrome is
maximised on this display (1366x768). Derived empirically from debug screenshot.
"""
import sys
import time
import ctypes
import ctypes.wintypes as wintypes
from PIL import ImageGrab

# Absolute screen-pixel coordinates of the story frame
STORY_SCREEN = (428, 138, 764, 703)  # top +40 to skip the Chrome debug banner


def focus_chrome():
    user32 = ctypes.windll.user32
    found_hwnd = None

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, lparam):
        nonlocal found_hwnd
        if not user32.IsWindowVisible(hwnd):
            return True
        buf = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(hwnd, buf, 512)
        title = buf.value
        if "Instagram" in title:
            found_hwnd = hwnd
            return False  # stop enumeration
        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)

    if found_hwnd is None:
        # Fallback: any Chrome window
        def cb2(hwnd, lparam):
            nonlocal found_hwnd
            if not user32.IsWindowVisible(hwnd):
                return True
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            if "Chrome" in buf.value:
                found_hwnd = hwnd
                return False
            return True
        user32.EnumWindows(EnumWindowsProc(cb2), 0)

    if found_hwnd is None:
        return False, "No Chrome/Instagram window found"

    user32.ShowWindow(found_hwnd, 9)   # SW_RESTORE
    user32.SetForegroundWindow(found_hwnd)
    time.sleep(0.6)
    return True, None


def capture_story(output_path):
    ok, err = focus_chrome()
    if not ok:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    img = ImageGrab.grab(bbox=STORY_SCREEN)
    img.save(output_path, "JPEG", quality=95)
    print(f"Saved: {output_path} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python capture_story.py <output_path>")
        sys.exit(1)
    capture_story(sys.argv[1])
