import unittest
from tools.frame_detector import FrameDetector


class TestFrameDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global tester
        tester = FrameDetector.FrameDetector()
