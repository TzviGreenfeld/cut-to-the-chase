import math
import pytesseract
import numpy as np
import cv2
import os
import time
from joblib import Parallel, delayed
from PIL import Image
from tqdm import tqdm
from datetime import datetime
start = datetime.now()


class FrameDetector:
    def __init__(self, frame):
        self.file = frame

    def find_text_in_frame():
        pass


def is_relevant(s):
    return s in s in "1234567890:"


def is_100(text):
    return "1:00" in text


output = "Size,Method,Frame,Time,\n"


def find_100(option, path, filename):
    global output
    img = cv2.imread(path + filename)

    start = datetime.now()
    inverted_image = cv2.bitwise_not(img)
    # cv2.imwrite("/home/tzvigr/chaser/tools/temp/inverted.jpg", inverted_image)
    text = pytesseract.image_to_string(
        inverted_image, config='--oem 3 --psm 12')
    text = ''.join(list(filter(is_relevant, text)))
    # print("\ninverted_image:", f"{text=}", "1:00" in text)
    if is_100(text):
        output += f"{option},inverted_image,{filename},{datetime.now() - start},\n"

    start = datetime.now()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("/home/tzvigr/chaser/tools/temp/gray.jpg", gray_image)
    text = pytesseract.image_to_string(
        gray_image, config='--oem 3 --psm 6')
    text = ''.join(list(filter(is_relevant, text)))
    # print("\ngray:", f"{text=}", "1:00" in text)
    if is_100(text):
        output += f"{option},gray_image,{filename},{datetime.now() - start},\n"

    start = datetime.now()
    thresh, im_bw = cv2.threshold(
        gray_image, 50, 230, cv2.THRESH_BINARY)
    # cv2.imwrite("/home/tzvigr/chaser/tools/temp/bw_image.jpg", im_bw)
    text = pytesseract.image_to_string(im_bw, config='--oem 3 --psm 6')
    text = ''.join(list(filter(is_relevant, text)))
    # print("\nim_bw:", f"{text=}", "1:00" in text)
    if is_100(text):
        output += f"{option},im_bw,{filename},{datetime.now() - start},\n"
    return


if __name__ == '__main__':
    options = ["medium", "small", "tiny"]

    for i, option in enumerate(options):
        print(f"Currently on {option} [{i + 1}/{len(options)}]")
        path = '/home/tzvigr/chaser/test/samples/' + option + "/"
        Parallel(n_jobs=-1)(delayed(find_100)(option, path, filename)
                            for filename in tqdm(os.listdir(path)))

    # output += f"-----TIME:\t ,{datetime.now() - start}-----"
    with open('/home/tzvigr/chaser/test/samples/' + "results.csv", "a+") as out:
        out.write(output)
