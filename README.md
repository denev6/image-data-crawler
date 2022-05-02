# Pincette

`selenium` 기반의 이미지 크롤링 및 처리 모듈

## Version

- python: 3.8.11  
- pillow: 9.0.1  
- selenium: 3.141.0  
- urllib3: 1.26.6  


## Example

```python
# Import pincette.py
from pincette import *

# Settings
gif_dir = make_dir("test", "crawled")
img_dir = make_dir("test", "imgs")
result_dir = make_dir("test", "converted")
driver = "chromedriver.exe"   # 0
url = "https://pincette.netlify.app/"

# Crawling and Processing
pn = Pincette(driver)   # 1
pn.load_page(url, scroll=False)   # 2
pn.find_imgs("image__content")   # 3
pn.save_imgs(gif_dir, progess=True)   # 4
pn.close_tab()   # 5
pn.gif_to_img(gif_dir, img_dir, copy_imgs=True)   # 6
pn.convert(img_dir, result_dir, img_size=(32, 32), gray_scale=True)   # 7
```
`#0`: 해당 코드는 <a href="https://chromedriver.chromium.org/downloads" target="_blank">Chrome-Driver</a>를 사용합니다.  
`#1`: driver 경로와 옵션 값을 설정합니다. 옵션은 생략할 수도 있습니다.  
`#2`: 크롤링을 수행하기 위해 페이지를 로딩합니다.  
`#3`: 이미지 주소를 태그의 class로 찾아 저장합니다.  
`#4`: 찾은 이미지를 저장합니다.  
`#5`: 브라우저와 driver를 종료합니다.  
`#6`: gif 파일을 여러 이미지로 나누어 줍니다.  
`#7`: 이미지의 크기를 조정하거나 색상을 회색조로 변경할 수 있습니다.  


자세한 설명은 docstring을 참고해 주세요.  
```python
>>> from pincette import *
>>> print(Pincette.__doc__)
...
>>> print(Pincette.load_page.__doc__)
...
>>> print(make_dir.__doc__)
...
```

**예시 이미지**

<img src="./pages/assets/readme-1.png" alt="크롤링 샘플">

resized:  
<img src="./pages/assets/readme-2.png" alt="크기 조정 결과">

grayscale:  
<img src="./pages/assets/readme-3.png" alt="회색조 변환 결과">

**예시 이미지(gif)**

<img src="./pages/assets/shape.gif" alt="크롤링 샘플 gif" width=130>

gif_to_img:  
<img src="./pages/assets/readme-4.png" alt="회색조 변환 결과">


## Use Selenium  

`Pincette`는 `driver`속성을 가지고 있으며, 이는 selenium의 `webdriver.Chrome`과 동일합니다.  
따라서 <a href="https://www.selenium.dev/documentation/webdriver/elements/finders/" target="_blank">selenium</a>의 함수를 그대로 사용할 수 있습니다.  
```python
pn = Pincette(driver_path)

element = pn.driver.find_element_by_class_name("content")
src = element.get_attribute("src")

pn.extend_srcs([src])
pn.save_imgs(...)
...
```


## Test

`index.html`: [테스트 페이지](https://pincette.netlify.app/)를 제공합니다.  
현재 _pincette.py_ 는 테스트 페이지를 크롤링할 수 있도록 작성되었습니다.  
  
```python
# pincette.py

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
```