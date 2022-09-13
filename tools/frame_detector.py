from datetime import datetime
from turtle import RawTurtle
import easyocr
import re
from tqdm import tqdm


class FrameDetector:
    def __init_(self, frames):
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frames = frames
        self.found = []
        self.detection_time = -1

    def detect(self):
        f = tqdm(self.frames)
        for frame in f:
            start = datetime.now()
            result = self.reader.readtext(frame)
            for rect, text, confidence in result:
                if re.match('1:00|2:00|2.00', text):
                    self.found.append((frame, text, confidence))

        self.detectionTime = f.t.format_dict["elapsed"]
        self.found.sort(key=lambda res: res[2], reverse=True)

    def get_best_results(self):
        time_stamps = []
        one_cnt, two_cnt = 0, 0
        for frame, text, confidence in self.found:
            if (text[0] == 1 and one_cnt < 4) or (text[0] == 2 and two_cnt == 0):
                time_stamps.append((frame, text))
        time_stamps.sort(key=lambda stamp: stamp[0][3:])
        return time_stamps


