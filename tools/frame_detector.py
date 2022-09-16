import easyocr
import re
import warnings
from datetime import datetime
from turtle import RawTurtle, st
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)


class FrameDetector:
    def __init__(self, frames):
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frames = frames
        self.found = []
        self.detection_time = -1

    def detect(self):
        f = tqdm(self.frames.items())
        for stamp, frame in f:
            result = self.reader.readtext(frame)
            for (rect, text, confidence) in result:
                if re.match('1.00|1:00|2:00|2.00', text):
                    self.found.append((stamp, rect, text, confidence))
                
        self.detectionTime = f.format_dict["elapsed"]
        self.found.sort(key=lambda res: res[2], reverse=True) # sort by confidence

    def get_best_results(self):
        # TODO: add parameter to make at least a minute between 2 good frames to remove duplicates
        # TODO: test more episodes to set cinfidence filter
        best_frames = []
        one_cnt, two_cnt = 0, 0
        last_stamp = 0
        for stamp, rect, text, confidence in self.found:
            if text[0] == '1' and one_cnt < 4 and not is_duplicate(best_frames, stamp):
                one_cnt += 1
                best_frames.append((stamp, rect, text, confidence))
            elif text[0] == '2' and two_cnt == 0 and not is_duplicate(best_frames, stamp):
                two_cnt += 1
                best_frames.append((stamp, rect, text, confidence))
        return best_frames

    def __str__(self) -> str:
        return f"Found {len(self.found)} time stamps in {self.detectionTime} seconds"
