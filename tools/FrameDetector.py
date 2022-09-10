from PIL import Image
import pytesseract
import numpy as np
import cv2



class FrameDetector:
    def __init__(self, frame):
        self.file = frame

    def find_text_in_frame():
        pass


if __name__ == '__main__':
    # filename = '/home/tzvigr/chaser/test/good_100_small.png'
    # filename = '/home/tzvigr/chaser/test/smaller.png'
    # filename = '/home/tzvigr/chaser/test/smallest.png'
    filename = '/home/tzvigr/chaser/test/good_100.png'
    img = cv2.imread(filename)

    inverted_image = cv2.bitwise_not(img)
    cv2.imwrite("/home/tzvigr/chaser/tools/temp/inverted.jpg", inverted_image)
    text = pytesseract.image_to_string(inverted_image, config='--oem 3 --psm 12')
    text = ''.join(list(filter(lambda s: s in "1234567890:", text)))
    print("\ninverted_image:", f"{text=}", "1:00" in text)

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/home/tzvigr/chaser/tools/temp/gray.jpg", gray_image)
    text = pytesseract.image_to_string(gray_image, config='--oem 3 --psm 6')
    text = ''.join(list(filter(lambda s: s in "1234567890:", text)))
    print("\ngray:", f"{text=}", "1:00" in text)


    thresh, im_bw = cv2.threshold(gray_image, 50, 230, cv2.THRESH_BINARY)
    cv2.imwrite("/home/tzvigr/chaser/tools/temp/bw_image.jpg", im_bw)
    text = pytesseract.image_to_string(im_bw, config='--oem 3 --psm 6')
    text = ''.join(list(filter(lambda s: s in "1234567890:", text)))
    print("\nim_bw:", f"{text=}", "1:00" in text)
    
