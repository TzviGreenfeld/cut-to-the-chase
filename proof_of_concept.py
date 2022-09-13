import easyocr
import re
import cv2
from tqdm import tqdm
from datetime import datetime



class FrameDetector:
    def __init_(self, frames):
        print("initaing")
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frames = frames
        self.found = []
        self.detection_time = -1


    def detect(self):
        print("started detecting")
        f = tqdm(self.frames)
        for i ,frame in enumerate(f):
            result = self.reader.readtext(frame)
            for rect, text, confidence in result:
                if re.match('1:00|2:00|2.00', text):
                    self.found.append((i, text, confidence))

        print("finished detecting, getting duration")
        self.detectionTime = f.t.format_dict["elapsed"]
        self.found.sort(key=lambda res: res[2], reverse=True)

    def get_best_results(self):
        print("getting best result")
        time_stamps = []
        one_cnt, two_cnt = 0, 0
        for frame_index, text, confidence in self.found:
            if (text[0] == 1 and one_cnt < 4) or (text[0] == 2 and two_cnt == 0):
                time_stamps.append([frame_index, text])
        print("sorting best result")
        time_stamps.sort(key=lambda stamp: stamp[0])
        for stamp in time_stamps:
            stamp[0] = str(datetime.timedelta(seconds= 2 * stamp[0]))
        return time_stamps


if __name__ == '__main__':
    video_name = "test/samples/sample_episode.mp4"
    vidcap = cv2.VideoCapture(video_name)
    success, image = vidcap.read()

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    h, w, _ = image.shape
    count = 0
    frames = []
    pbar = tqdm(total=74200)
    while success:
        if count % 2*fps == 0:  # every 2 seconds
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            frames.append(image[h//2:h, w//2:w])

        success, image = vidcap.read()
        count += 1
        pbar.update(1)
    vidcap.release()
    pbar.close()
 #TODO: why does program "6702 killed" here
    print("detecort init from main")
    detector = FrameDetector(frames)
    detector.detect()
    print(detector.get_best_results())
