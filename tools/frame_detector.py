import easyocr
import re
import warnings
from datetime import datetime
from turtle import RawTurtle
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)


class FrameDetector:
    def __init__(self, frames):
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frames = frames
        self.found = []
        self.detection_time = -1

    def detect(self):
        f = tqdm(self.frames)
        for i, frame in enumerate(f):
            start = datetime.now()
            result = self.reader.readtext(frame)
            for (rect, text, confidence) in result:
                if re.match('1.00|1:00|2:00|2.00', text):
                    self.found.append((i, text, confidence))

        self.detectionTime = f.format_dict["elapsed"]
        self.found.sort(key=lambda res: res[2], reverse=True)
        print(f"{self.found=}")

    def get_best_results(self):
        time_stamps = []
        one_cnt, two_cnt = 0, 0
        for frame, text, confidence in self.found:
            if (text[0] == '1' and one_cnt < 4):
                one_cnt += 1
                time_stamps.append((frame, text))
            elif (text[0] == '2' and two_cnt == 0):
                two_cnt += 1
                time_stamps.append((frame, text))
        return time_stamps

    def __str__(self) -> str:
        return f"Found {len(self.found)} time stamps in {self.detectionTime} seconds"
