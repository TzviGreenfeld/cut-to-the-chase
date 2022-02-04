import cv2
import numpy as np
import pyautogui


def test(needle_image, haystack_image):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    try:
        loc = pyautogui.locate(template.astype(np.uint8), img_gray.astype(np.uint8), grayscale=True)
        print(loc)
    except pyautogui.ImageNotFoundException:
        print("img not found")


if __name__ == '__main__':
    needle_image = open("1_min")
    haystack_image = ""
    test(needle_image, haystack_image)
