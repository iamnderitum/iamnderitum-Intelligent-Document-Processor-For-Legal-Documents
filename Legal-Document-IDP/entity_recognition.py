import pytesseract
from pytesseract import *

from PIL import Image

def read_image():
    image = Image.open("front_image.png")
    img_txt = pytesseract.image_to_string(image)
    print(img_txt)