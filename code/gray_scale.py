import os
from pathlib import Path

from PIL import Image

CWD = os.getcwd()
IMG_DIR = os.path.join(CWD, "result", "converted")  # 이미지 경로 변경하여 사용
SAVE_DIR = os.path.join(CWD, "result", "grayscale")  # 저장 경로 변경하여 사용
os.makedirs(SAVE_DIR, exist_ok=True)


def specify_img_path(file_name):
    return os.path.join(IMG_DIR, file_name)


def specify_save_path(file_name):
    return os.path.join(SAVE_DIR, f"{Path(file_name).stem}.png")


imgs = os.listdir(IMG_DIR)
imgs = list(map(specify_img_path, imgs))

for img in imgs:
    with Image.open(img) as img_:
        grayscale = img_.convert("L")
        grayscale.save(specify_save_path(img))
