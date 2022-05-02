import os
import shutil
from pathlib import Path

from PIL import Image

CWD = os.getcwd()
GIF_DIR = os.path.join(CWD, "sample")
SAVE_DIR = os.path.join(CWD, "result", "converted")
os.makedirs(SAVE_DIR, exist_ok=True)


def find_ext(extension):
    file = f"*.{extension}"
    return list(Path(GIF_DIR).glob(file))


gifs = find_ext("gif")
imgs = find_ext("png") + find_ext("jpg")

for gif in gifs:
    with Image.open(gif) as gif_:
        for n_frame in range(gif_.n_frames):
            gif_.seek(n_frame)
            file_name = f"{Path(gif).stem}-{n_frame}.png"
            file_path = os.path.join(SAVE_DIR, file_name)
            gif_.save(file_path)

for img in imgs:
    shutil.copy(img, SAVE_DIR)

