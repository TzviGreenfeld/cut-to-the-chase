import easyocr
import re
import cv2
from tqdm import tqdm
from datetime import datetime
from tools.frame_detector import FrameDetector


if __name__ == '__main__':
    video_name = "/home/tzvigr/chaser/test/samples/sample_episode.mp4"
    vidcap = cv2.VideoCapture(video_name)
    success, image = vidcap.read()
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    h, w, _ = image.shape
    count = 0
    frames = []

    # get some frames as np array
    pbar = tqdm(total=int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while success:
        if count % (2 * fps) == 0:  # every 2 seconds
            success, image = vidcap.read()
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                frames.append(image[h//2:h, w//2:w])
        else:
            ret = vidcap.grab()
        count += 1
        pbar.update(1)

    pbar.close()

    detector = FrameDetector(frames)
    detector.detect()
    print(f"{detector.get_best_results()=}")

    vidcap.release()
