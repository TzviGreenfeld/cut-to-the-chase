import cv2
import numpy as np
from tools.videoTools import Editor

import cv2


def resize(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def show_similarities(img1, img2):
    img1 = cv2.imread(img1, 0)
    img2 = cv2.imread(img2, 0)
    # img1, img2 = resize(img1, 60), resize(img2, 60)
    orb = cv2.ORB_create(nfeatures=100000)
    keypoints, descriptor = orb.detectAndCompute(img1, None)
    frmae_keypoints, frmae_descriptor = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptor, frmae_descriptor, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    out = cv2.drawMatchesKnn(img1, keypoints, img2, frmae_keypoints, good, None, flags=2)
    cv2.imshow("out", out)
    cv2.waitKey(0)


def get_bottom_half(img):
    height, width = img.shape
    cropped_image = img[int(height / 2):height, 0:width]
    return cropped_image


def locate_pic_in_frame(img_file, frame_file):
    # load
    img = cv2.imread(img_file, 0)
    frame = cv2.imread(frame_file, 0)

    # crop to improve results
    frame = get_bottom_half(frame)

    # compare
    orb = cv2.ORB_create()
    keypoints, descriptor = orb.detectAndCompute(img, None)
    frmae_keypoints, frmae_descriptor = orb.detectAndCompute(frame, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptor, frmae_descriptor, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    print(len(good))

    # show
    out = cv2.drawMatchesKnn(img, keypoints, frame, frmae_keypoints, good, None, flags=2)
    cv2.imshow("out", out)
    cv2.waitKey(0)


def is_in_frame(img, frame):
    # crop to improve results
    frame = get_bottom_half(frame)

    # compare
    orb = cv2.ORB_create(nfeatures=9900000)
    keypoints, descriptor = orb.detectAndCompute(img, None)
    frame_keypoints, frame_descriptor = orb.detectAndCompute(frame, None)

    bf = cv2.BFMatcher()
    if descriptor is None or frame_descriptor is None:
        return

    good = []
    matches = bf.knnMatch(descriptor, frame_descriptor, k=2)
    try:
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])
    except:
        return
    if len(good) > 10:
        # cv2.imshow("FOUND", frame)
        # cv2.waitKey(0)
        print(len(good))
        out = cv2.drawMatchesKnn(img, keypoints, frame, frame_keypoints, good, None, flags=2)
        cv2.imshow("out", out)
        cv2.waitKey(0)
        return True


if __name__ == '__main__':
    img_path = r"D:\code\chaser\test\US\1_min.png"
    frame0 = r"D:\code\chaser\test\US\FALSE0.png"
    frame1 = r"D:\code\chaser\test\US\FALSE1.png"
    frame2 = r"D:\code\chaser\test\US\TRUE0.png"
    frame3 = r"D:\code\chaser\test\US\TRUE1.png"
    frames = [frame1, frame2, frame3, frame0]

    vid_path = r"D:\code\chaser\test\US\The.Chase.US.S02E17.720p.WEB.h264-KOGi.mkv"

    # locate_pic_in_frame(img_path, frame2)
    # for frame in frames:
    #     locate_pic_in_frame(img_path, frame)
    img = cv2.imread(img_path, 0)
    cap = cv2.VideoCapture(vid_path)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        i += 1
        if i % 60 == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if is_in_frame(img, frame):
                print(f"found in: {i/60} seconds")
