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

    def __gt__(self, other):
        """
        Compare two frames by confidence
        this is used to sort the frames and only keep the best ones
        """
        return self.confidence > other.confidence

    def min_time_diff(self, others):
        """
        Return the minimum time difference in seconds between this frame and the others
        """
        min_delta = 99999
        for frame in others:
            t1 = self.stamp
            t2 = frame.stamp
            delta = max(t1, t2) - min(t1, t2)
            min_delta = min(delta, min_delta)
        return min_delta

    def __repr__(self):
        out = ""
        out += "time: {}\t".format(self.stamp)
        out += "text: {}\t".format(self.text)
        out += "confidence: {}".format(self.confidence)
        return out


class FrameDetector:
    def __init__(self, frames):
        """
        Create a FrameDetector object
        :param frames (dict): a dictionary of frames with the key being the timestamp
        """
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.frames = frames
        self.found = []
        self.detection_time = -1


    def detect(self):
        """
        Detect which frmaes contain one or two minute timer
        """
        f = tqdm(self.frames.items())
        for stamp, frame in f:
            result = self.reader.readtext(frame)
            for (rect, text, confidence) in result:
                if re.match('1.00|1:00|2:00|2.00', text): # somtimes easyOCR returns 1.00 instead of 1:00
                    self.found.append(Frame(stamp, rect, text, confidence))

        self.detectionTime = f.format_dict["elapsed"]
        # sort by confidence
        self.found.sort(reverse=True)

    def get_best_results(self):
        """
        Return the relevant frames, and removes duplicates
        """
        # TODO: test more episodes to set cinfidence filter
        best_frames = []
        one_cnt, two_cnt = 0, 0
        counts = [one_cnt, two_cnt]
        # TODO: this is so ugly, fix it
        for frame in self.found:
            curr = 0 if frame.text[0] == '1' else 1
            if ((counts[curr] > 0 and frame.min_time_diff(best_frames) > 120) or
                    counts[curr] == 0):
                best_frames.append(frame)
                counts[curr] += 1
        return best_frames

    def __str__(self) -> str:
        return f"Found {len(self.found)} frames in {self.detectionTime} seconds"
