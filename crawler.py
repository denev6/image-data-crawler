import os
from datetime import date
from time import sleep

from selenium import webdriver
from urllib.request import urlretrieve

# LOCAL PATH
CWD = os.getcwd()
DRIVER_PATH = os.path.join(CWD, "driver.exe")  # driver 경로 변경하여 사용
SAVE_DIR = os.path.join(CWD, "images")  # 저장 경로 변경하여 사용
os.makedirs(SAVE_DIR, exist_ok=True)

# URL
URL = ""  # URL 경로 변경하여 사용

# SCROLL
PAUSE = 5
MAX_ITER = 3

# DATE
today = date.today()
DATE = f"{today.month:02}{today.day:02}"

# CRAWLER: user agent를 설정할 경우, 아래 주석을 해제한 후 USER_AGENT 입력
# USER_AGENT = ""
# options = webdriver.ChromeOptions()
# options.add_argument(USER_AGENT)
# browser = webdriver.Chrome(DRIVER_PATH, options=options)

browser = webdriver.Chrome(DRIVER_PATH)
browser.implicitly_wait(3)
browser.maximize_window()

browser.get(URL)

prev_height = 0
for _ in range(MAX_ITER):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    sleep(PAUSE)

    curr_height = browser.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break

    prev_height = curr_height


# 사용자 필요에 따라 아래에 코드 설정
# 이미지의 src 태그가 포함된 코드를 찾아 imgs로 저장
imgs = browser.find_elements_by_class_name("...")
alts = browser.find_element_by_class_name("...")

img_srcs = list()

for img in imgs:
    src = img.get_attribute("src")
    img_srcs.append(src)

for i, url in enumerate(img_srcs):
    extension = str(url).rfind(".")
    file_name = f"{DATE}-{i}" + url[extension:]
    # print(alts[i])
    urlretrieve(url, os.path.join(SAVE_DIR, file_name))
