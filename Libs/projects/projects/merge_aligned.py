from PIL import Image
import numpy as np
import cv2
import os

FOLDER = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll project"
OUTPUT = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_aligned.jpg"

target_h = 1129

imgs_pil = [Image.open(os.path.join(FOLDER, f"{i}.jpg")).convert("RGB") for i in range(1, 11)]
imgs = [img.resize((int(img.width * target_h / img.height), target_h), Image.LANCZOS) for img in imgs_pil]

# Seam parameters: (x-overlap px, y-shift px)
# Detected via NCC grid-search on equalized edge strips (max_dy=400).
# Seam 5 overridden to dy=0: NCC gave +90 but CM-based check showed content
# centers already at y=605 vs 603 (false positive from different-scene seam).
seam_params = [
    (10,  +20),  # 1→2
    (10,  +25),  # 2→3
    (40,   -5),  # 3→4
    (90,  -10),  # 4→5
    (60,    0),  # 5→6  (overridden)
    (10,  -20),  # 6→7
    (35,  -15),  # 7→8
    (30,  -10),  # 8→9
    (15,  +10),  # 9→10
]
ovs = [p[0] for p in seam_params]
dys = [p[1] for p in seam_params]

print("=== Seam parameters ===")
for i, (ov, dy) in enumerate(seam_params):
    print(f"  Seam {i+1}->{i+2}: ov={ov}px  dy={dy:+d}px")

# Cumulative canvas positions
xs, ys = [0], [0]
for i in range(len(imgs) - 1):
    xs.append(xs[-1] + imgs[i].width - ovs[i])
    ys.append(ys[-1] + dys[i])

y_min = min(ys)
ys = [y - y_min for y in ys]

canvas_w = xs[-1] + imgs[-1].width
canvas_h = max(y + target_h for y in ys)

print(f"\nCanvas: {canvas_w} x {canvas_h} px")
print(f"  x positions: {xs}")
print(f"  y positions: {ys}")

canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))

# Paste left-to-right; each image overwrites the overlap strip from the previous
for i, img in enumerate(imgs):
    canvas.paste(img, (xs[i], ys[i]))

canvas.save(OUTPUT, "JPEG", quality=95)
print(f"\nSaved: {OUTPUT}")
