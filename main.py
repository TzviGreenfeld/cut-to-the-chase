import sys
import cv2
import numpy as np
from cv2.cv2 import CAP_PROP_POS_MSEC
import pyautogui


def show_image(img):
    cv2.imshow("~hi~", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_img(img_rgb, template, count):
    # find if a photo is in frame
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    try:
        loc = pyautogui.locate(template.astype(np.uint8), img_gray.astype(np.uint8), grayscale=True)
        print(loc)
    except pyautogui.ImageNotFoundException:
        pass


def millis_to_mmss(milliseconds):
    millis = int(milliseconds)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    return (minutes, seconds)


def get_time_stamps(vid_path, img_path):
    vidcap = cv2.VideoCapture(vid_path)
    template = cv2.imread(img_path, 0)  # open template only once
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break  # loop and a half construct is useful
        if count % 60 == 0:
            curr_time_stamp = vidcap.get(CAP_PROP_POS_MSEC)
            print('Read a new frame: ', success, " time: ", millis_to_mmss(curr_time_stamp))
            process_img(image, template, count)
        count += 1


def calc_good_parts(good_time_stamps):
    pass


def delete_clips(full_vid):
    pass


def main(args):
    # load episode
    if len(args) < 2:
        print("Please insert video path")
        return

    full_video_path = args[1]
    get_time_stamps(full_video_path, "resources/1_min.png")


if __name__ == '__main__':
    main(sys.argv)
