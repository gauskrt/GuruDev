from PIL import Image
import os

FOLDER = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll project"
OUTPUT = r"C:\Users\user\Desktop\Gaurav\GuruDev\Libs\projects\projects\scroll_merged.jpg"

images = [Image.open(os.path.join(FOLDER, f"{i}.jpg")).convert("RGB") for i in range(1, 11)]

target_h = int(sum(img.height for img in images) / len(images))  # average height

resized = [img.resize((int(img.width * target_h / img.height), target_h), Image.LANCZOS) for img in images]

total_w = sum(img.width for img in resized)
canvas = Image.new("RGB", (total_w, target_h), (255, 255, 255))

x = 0
for img in resized:
    canvas.paste(img, (x, 0))
    x += img.width

canvas.save(OUTPUT, "JPEG", quality=95)
print(f"Saved: {OUTPUT}  ({total_w} x {target_h} px)")
