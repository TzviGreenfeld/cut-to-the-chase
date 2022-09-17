import easyocr
import re
import warnings
from datetime import datetime, timedelta
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning)
class Frame:
    def __init__(self, stamp, rect, text, confidence):
        self.stamp = stamp
        self.rect = rect
        self.text = text
        self.confidence = confidence

    def __gt__(self, other): # by confidence
        return self.confidence > other.confidence
    
    def min_time_diff(self, others): # by time
        min_delta = timedelta(seconds=99999)
        for frame in others:
            t1 = datetime.strptime(self.stamp, "%M:%S")
            t2 = datetime.strptime(frame.stamp, '%M:%S')
            delta = max(t1, t2) - min(t1, t2)
            min_delta = min(delta, min_delta)
        return min_delta.seconds

    def __repr__(self):
        out = ""
        out += "time: {}\t".format(self.stamp)
        out += "text: {}\t".format(self.text)
        out += "confidence: {}".format(self.confidence)
        return out



        

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
                    self.found.append(Frame(stamp, rect, text, confidence))

        self.detectionTime = f.format_dict["elapsed"]
        # sort by confidence
        self.found.sort(reverse=True)

    def get_best_results(self):
        # TODO: test more episodes to set cinfidence filter
        best_frames = []
        one_cnt, two_cnt = 0, 0
        counts = [one_cnt, two_cnt]
        for frame in self.found:
            curr = 0 if frame.text[0] == '1' else 1
            if ((counts[curr] > 0 and frame.min_time_diff(best_frames) > 60) or
                counts[curr] == 0):
                best_frames.append(frame)
                counts[curr] += 1
        return best_frames

    def __str__(self) -> str:
        return f"Found {len(self.found)} time stamps in {self.detectionTime} seconds"
