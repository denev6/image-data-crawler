import os
from pathlib import Path

from PIL import Image

CWD = os.getcwd()
IMG_DIR = os.path.join(CWD, "result", "converted")
SAVE_DIR = os.path.join(CWD, "result", "grayscale")
os.makedirs(SAVE_DIR, exist_ok=True)


def specify_img_path(file_name):
    return os.path.join(IMG_DIR, file_name)


def specify_save_path(file_name):
    return os.path.join(SAVE_DIR, f"{Path(file_name).stem}.png")


imgs = os.listdir(IMG_DIR)
imgs = list(map(specify_img_path, imgs))

for img in imgs:
    with Image.open(img) as f:
        grayscale = f.convert("L")
        grayscale.save(specify_save_path(img))
