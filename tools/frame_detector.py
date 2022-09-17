import easyocr
import re
import warnings
from datetime import datetime, timedelta
from turtle import RawTurtle, st
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)
class Frame:
    def __init__(self, stamp, rect, text, confidence):
        self.stamp = stamp
        self.rect = rect
        self.text = text
        self.confidence = confidence

    def __gt__(self, other): # by confidence
        return self.confidence > other.cnfidence
    
    def __sub__(self, other): # by time
        t1 = datetime.fromtimestamp(self.stamp).strftime('%M:%S')
        t2 = datetime.fromtimestamp(other.stamp).strftime('%M:%S')
        delta = datetime.strptime(
            max(t1, t2), '%M:%S') - datetime.strptime(min(t1, t2), '%M:%S')
        return delta.total_seconds()


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
        # sort by confidence
        self.found.sort(key=lambda res: res[3], reverse=True)

    def get_best_results(self):
        def time_diff(existing_frames, new_frame_time):
            min_delta = timedelta(minutes=1000)
            for frame in existing_frames:
                t1 = datetime.fromtimestamp(frame[0]).strftime('%M:%S')
                t2 = datetime.fromtimestamp(new_frame_time).strftime('%M:%S')
                delta = datetime.strptime(
                    max(t1, t2), '%M:%S') - datetime.strptime(min(t1, t2), '%M:%S')
                min_delta = min(delta, min_delta)
            return min_delta

        # TODO: test more episodes to set cinfidence filter
        best_frames = []
        one_cnt, two_cnt = 0, 0
        last_stamp = 0

        for stamp, rect, text, confidence in self.found:
            if (text[0] == '1' and
                one_cnt < 4 and
                time_diff(best_frames, stamp) > timedelta(minutes=1)):
                one_cnt += 1
                best_frames.append((stamp, rect, text, confidence))

            elif (text[0] == '2' and
                  two_cnt == 0 and
                  time_diff(best_frames, stamp) > timedelta(minutes=1)):
                two_cnt += 1
                best_frames.append((stamp, rect, text, confidence))
        return best_frames

    def __str__(self) -> str:
        return f"Found {len(self.found)} time stamps in {self.detectionTime} seconds"
