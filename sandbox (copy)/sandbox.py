import os

import cv2
import numpy as np
import pyautogui


def show_image(img):
    cv2.imshow("~hi~", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test(needle, haystack):
    needle_ = cv2.imread(needle)
    haystack_ = cv2.imread(haystack)
    try:
        loc = pyautogui.locate(needle, haystack, grayscale=True)
        if loc is not None:
            print(loc)
    except pyautogui.ImageNotFoundException:
        print("img not found")


if __name__ == '__main__':
    # needle_image = open("1_min.png", "r")
    # haystack_image = open("haystack/hayStack_1MIN.png", "r")
    PATH = "/users/studs/bsc/2022/tzvigree/Documents/sandbox/haystack/"
    two_min_needle_image = "/users/studs/bsc/2022/tzvigree/Documents/sandbox/2_min.png"
    one_min_needle_image = "/users/studs/bsc/2022/tzvigree/Documents/sandbox/1_min.png"
    prev_one_min_needle_image = "/users/studs/bsc/2022/tzvigree/Documents/sandbox/prev_1_min.png"

    for filename in os.listdir(PATH):
        print(filename + ":")
        haystack_image = PATH + filename

        test(two_min_needle_image, haystack_image)
        test(one_min_needle_image, haystack_image)
        test(prev_one_min_needle_image, haystack_image)
