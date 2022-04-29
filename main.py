import os
import shutil
from pathlib import Path
from time import sleep
from collections.abc import Sequence

from PIL import Image
from selenium import webdriver
from urllib.request import urlretrieve


class ImgCrawler(object):
    def __init__(self, driver_path, user_agent):
        options = webdriver.ChromeOptions()
        options.add_argument(user_agent)
        self._driver = webdriver.Chrome(driver_path, options=options)

    def crawl_img(self, url, save_dir, scroll=False, iter=3, pause=3):
        """이미지 데이터 크롤링을 수행한다. (사용자 필요에 따라 코드 수정 필요)
        
            Args:
                url: (str) 크롤링을 수행할 URL
                save_dir: (str) 저장할 파일 경로
                scroll: (bool) 스크롤 동작을 수행할 여부
                iter: (int) 스크롤 반복 횟수
                pause: (int) 스크롤 후 대기 시간(초)
        """
        self._driver.implicitly_wait(5)
        self._driver.maximize_window()
        self._driver.get(url)
        if scroll:
            self._scroll_down(iter, pause)

        ###################################################################
        # 사용자 필요에 따라 생성 및 조정
        # img_srcs: 이미지 파일 URL
        # file_name: (str, list, tuple) 이미지가 저장될 이름.
        #            None일 경우 0부터 정수 형식으로 자동 생성

        imgs = self._driver.find_elements_by_class_name("image__content")
        img_srcs = self._get_src(imgs)
        file_name = None

        ###################################################################

        self._save_img(img_srcs, save_dir, file_name)

        self._driver.quit()

    def convert(self, img_dir, save_dir, img_size=False, gray_scale=False):
        """이미지 데이터 크롤링을 수행한다. (사용자 필요에 따라 코드 수정 필요)
        
            Args:
                img_dir: (str) 원본 이미지 파일 경로
                save_dir: (str) 저장할 파일 경로
                img_size: (tuple[int:int]) 이미지 크기 (수행하지 않을 경우 False)
                gray_scale: (bool) 회색조 변경 수행 여부
        """
        imgs = []
        for ext in ("png", "jpg", "jpeg"):
            imgs += self._get_files(img_dir, ext)

        for img in imgs:
            with Image.open(img) as f:
                save_path = os.path.join(save_dir, f"{Path(img).stem}.png")
                if img_size:
                    f = f.resize(img_size)
                if gray_scale:
                    f = f.convert("L")
                f.save(save_path)

    def gif_to_png(self, gif_dir, save_dir, copy_imgs=False):
        """gif 파일을 png 이미지로 변환
        
            Args:
                gif_dir: (str) 원본 gif 파일 경로
                save_dir: (str) 저장할 파일 경로
                copy_imgs: (bool) gif 외 이미지 파일의 복사 여부
        """
        gifs = self._get_files(gif_dir, "gif")
        for gif in gifs:
            with Image.open(gif) as f:
                for n_frame in range(f.n_frames):
                    f.seek(n_frame)
                    file_name = f"{Path(gif).stem}-{n_frame}.png"
                    file_path = os.path.join(save_dir, file_name)
                    f.save(file_path)

        if copy_imgs:
            imgs = []
            for ext in ("png", "jpg", "jpeg"):
                imgs += self._get_files(gif_dir, ext)

            for img in imgs:
                shutil.copy(img, save_dir)

    def _scroll_down(self, max_iter, pause):
        previous_height = 0
        for _ in range(max_iter):
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            sleep(pause)
            current_height = self._driver.execute_script(
                "return document.body.scrollHeight"
            )
            if current_height == previous_height:
                break
            previous_height = current_height

    def _get_src(self, elements) -> list:
        """img 태그에서 src 반환
        
            Example:
                >>> imgs = self._driver.find_elements_by_class_name("image__content")
                >>> img_srcs =  self._get_src(imgs)
                >>> img_srcs
                ['http://...', 'http://...', 'http://...']
        """
        img_srcs = list()
        for img in elements:
            src = img.get_attribute("src")
            img_srcs.append(src)
        return img_srcs

    def _save_img(self, img_srcs, save_dir, file_name=None, print_=False):
        for i, url in enumerate(img_srcs):
            file_name = self._select_filename(file_name, i)
            extension = Path(url).suffix
            file = str(file_name) + extension
            urlretrieve(url, os.path.join(save_dir, file))
            if print_:
                print(file)

    def _select_filename(self, file_name, i):
        if isinstance(file_name, str):
            return f"{file_name}-{i}"
        elif isinstance(file_name, Sequence):
            return file_name[i]
        else:
            return i

    def _get_files(self, dir, extension):
        return list(Path(dir).glob(f"*.{extension}"))


if __name__ == "__main__":

    # 현재 경로
    CWD = os.getcwd()

    def make_dir(*file_name):
        dir = os.path.join(CWD, *file_name)
        os.makedirs(dir, exist_ok=True)
        return dir

    # 설정 값
    gif_dir = make_dir("test", "crawled")
    img_dir = make_dir("test", "imgs")
    result_dir = make_dir("test", "converted")
    driver = "driver.exe"
    user_agent = "..."
    url = "..."

    # 작업 수행
    ic = ImgCrawler(driver, user_agent)
    ic.crawl_img(url, gif_dir, scroll=True, iter=2)
    ic.gif_to_png(gif_dir, img_dir, copy_imgs=True)
    ic.convert(img_dir, result_dir, img_size=(32, 32), gray_scale=True)
