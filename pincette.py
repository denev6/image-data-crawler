import os
import shutil
from pathlib import Path
from time import sleep
from collections.abc import Sequence

from PIL import Image
from selenium import webdriver
from urllib.request import urlretrieve


class Pincette(object):
    """
    이미지 크롤링 및 처리를 위한 함수를 제공합니다.
       * Chrome driver를 사용하고 있습니다.

    Args:
        driver_path (str): 사용할 driver의 경로.
        *options: driver에 적용될 설정들. ChromeOptions.add_argument에 사용.

    Attributes:
        driver: selenium.webdriver.Chrome

    Functions:
        load_page
        find_imgs
        save_imgs
        gif_to_img
        convert
        extend_srcs

    Example:
        >>> from pincette import Pincette
        >>> ...
        >>> pn = Pincette(driver)
        >>> pn.load_page(url, scroll=False)
        >>> pn.find_imgs("image__content")
        >>> pn.save_imgs(gif_dir, progess=True)
        >>> pn.close_tab()
        >>> pn.gif_to_img(gif_dir, img_dir, copy_imgs=True)
        >>> pn.convert(img_dir, result_dir, img_size=(32, 32), gray_scale=True)
    """

    def __init__(self, driver_path, *options):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if options:
            for option in options:
                driver_options.add_argument(option)
        self.driver = webdriver.Chrome(driver_path, options=driver_options)
        self.__img_srcs = []

    def load_page(self, url, scroll=False, iter=3, pause=3):
        """
        크롤링을 위한 페이지 가져오기.
        
        Args:
            url (str): 크롤링을 수행할 URL.
            scroll (bool): 스크롤 동작을 수행할 여부.
            iter (int): 스크롤 반복 횟수.
            pause (int): 스크롤 후 대기 시간(초).
        """
        self.driver.implicitly_wait(5)
        self.driver.get(url)
        if scroll:
            self._scroll_down(iter, pause)

    def find_imgs(self, class_name, attr="src"):
        """
        크롤링할 이미지의 주소를 저장
        
        Args:
            class_name (str): 이미지 주소가 포함된 태그의 class.
            attr (str): 주소가 포함된 태그의 속성값.
        """
        imgs = self.driver.find_elements_by_class_name(class_name)
        img_srcs = self._get_attrs(imgs, attr)
        self.__img_srcs += img_srcs

    def save_imgs(
        self, save_dir, file_name=None, ext="auto", ignore=True, progess=False, max=None
    ):
        """
        주소를 통해 이미지 저장.
        
        Args:
            save_dir (str): 이미지 저장 경로.
            file_name (list, tuple, str): 저장할 이미지 파일 이름. 
                list 또는 tuple을 사용할 경우 순서대로 이름이 지정되며,
                str을 사용할 경우 str-{숫자} 형식으로 이름이 지정됩니다.
                기본값은 0, 1, 2 ... 과 같이 지정됩니다. 
            ext (str): 확장자 설정. 기본값은 크롤링하는 이미지에 따라 자동 설정.
            ignore (bool): 발생하는 예외를 무시할지 여부.
            progress (bool): 진행 상황의 실시간 출력 여부.
            max (int): 저장할 이미지의 최대 갯수 제한. 기본값은 제한을 두지 않음.
        """
        count = 0

        for i, url in enumerate(self.__img_srcs):
            label = self._select_filename(file_name, i)
            if ext == "auto":
                extension = Path(url).suffix
            else:
                extension = self._format_ext(ext)
            file = str(label) + extension
            try:
                urlretrieve(url, os.path.join(save_dir, file))
                count += 1
                if progess:
                    print(f"{i}: {file}")
            except Exception as exp:
                if not ignore:
                    raise exp
                print(f"'{file}'이 저장되지 못했습니다.")

            if count == max:
                return

    def extend_srcs(self, srcs):
        """
        selenium을 활용해 직접 주소를 가져왔을 때, 저장 목록에 해당 주소를 저장. 
        
        Args:
            srcs (list): 이미지 주소가 포함된 리스트.
        """
        self.__img_srcs += srcs

    def close_tab(self):
        """
        브라우저와 driver를 종료.
        """
        self.driver.quit()

    def gif_to_img(self, gif_dir, save_dir, ext="png", copy_imgs=False):
        """
        gif 파일을 이미지로 변환.
        
        Args:
            gif_dir (str): 원본 gif 파일 경로.
            save_dir (str): 저장할 파일 경로.
            ext (str): 저장할 이미지 확장자. 기본값은 png.
            copy_imgs (bool): gif 외 이미지 파일의 복사 여부.
        """
        ext = self._format_ext(ext)
        gifs = self._get_files(gif_dir, "gif")
        for gif in gifs:
            with Image.open(gif) as f:
                for n_frame in range(f.n_frames):
                    f.seek(n_frame)
                    file_name = f"{Path(gif).stem}-{n_frame}{ext}"
                    file_path = os.path.join(save_dir, file_name)
                    f.save(file_path)

        if copy_imgs:
            imgs = []
            for extension in ("png", "jpg", "jpeg"):
                imgs += self._get_files(gif_dir, extension)

            for img in imgs:
                shutil.copy(img, save_dir)

    def convert(self, img_dir, save_dir, img_size=False, gray_scale=False):
        """
        이미지 편집(크기 조정/회색조)을 수행.
        
        Args:
            img_dir (str): 원본 이미지 파일 경로.
            save_dir (str): 저장할 파일 경로.
            img_size (tuple[int:int]): 이미지 크기 (수행하지 않을 경우 False).
            gray_scale (bool): 회색조 변경 수행 여부.
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

    def _scroll_down(self, max_iter, pause):
        previous_height = 0
        for _ in range(max_iter):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(pause)
            current_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if current_height == previous_height:
                break
            previous_height = current_height

    def _get_attrs(self, elements, attr) -> list:
        img_srcs = list()
        for img in elements:
            src = img.get_attribute(attr)
            img_srcs.append(src)
        return img_srcs

    def _select_filename(self, file_name, i):
        if isinstance(file_name, str):
            return f"{file_name}-{i}"
        elif isinstance(file_name, Sequence):
            return file_name[i]
        else:
            return i

    def _get_files(self, dir, extension):
        return list(Path(dir).glob(f"*.{extension}"))

    def _format_ext(self, extention):
        if extention[0] == ".":
            return extention
        else:
            return f".{extention}"


def make_dir(*file_name):
    """
    파일을 생성하고 절대 경로를 반환.

    Args:
        *file_name (str): 현재 작업 디렉토리로부터의 경로.
    
    Returns:
        str: 생성된 파일의 절대 경로.

    Example:
        현재 작업 경로: 'C:\\a'
        >>> path = make_dir("b", "c", "d")
        >>> path
        'C:\\a\\b\\c\\d'
    """
    cwd = os.getcwd()
    dir = os.path.join(cwd, *file_name)
    os.makedirs(dir, exist_ok=True)
    return dir


if __name__ == "__main__":

    # 설정 값
    gif_dir = make_dir("test", "crawled")
    img_dir = make_dir("test", "imgs")
    result_dir = make_dir("test", "converted")
    driver = "chromedriver.exe"
    url = "https://pincette.netlify.app/"

    # 작업 수행
    pn = Pincette(driver, "window-size=1920,1080", "--disable-gpu")
    pn.load_page(url, scroll=False)
    pn.find_imgs("image__content")
    pn.save_imgs(gif_dir, progess=True)
    pn.close_tab()
    pn.gif_to_img(gif_dir, img_dir, copy_imgs=True)
    pn.convert(img_dir, result_dir, img_size=(32, 32), gray_scale=True)
