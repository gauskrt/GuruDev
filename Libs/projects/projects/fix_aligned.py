from PIL import Image
import numpy as np

INPUT  = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_aligned.jpg"
OUTPUT = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_aligned_fixed.jpg"

# Reproduce the same y positions from merge_aligned.py
target_h = 1129
dys = [+20, +25, -5, -10, 0, -20, -15, -10, +10]

ys = [0]
for dy in dys:
    ys.append(ys[-1] + dy)

y_min = min(ys)
ys = [y - y_min for y in ys]

# The region where ALL panels are present:
#   top    = the highest starting y (max of ys)
#   bottom = the lowest ending y   (min of y + target_h)
crop_top    = max(ys)
crop_bottom = min(y + target_h for y in ys)

print(f"y positions: {ys}")
print(f"Cropping rows {crop_top} to {crop_bottom}  (height {crop_bottom - crop_top})")

img = Image.open(INPUT)
print(f"Input size: {img.width} x {img.height}")

cropped = img.crop((0, crop_top, img.width, crop_bottom))
cropped.save(OUTPUT, "JPEG", quality=95)
print(f"Saved: {OUTPUT}  ({cropped.width} x {cropped.height})")
