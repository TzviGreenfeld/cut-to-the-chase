import unittest
from tools import FrameDetector
from tools.videoTools import Editor

class TestEditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global tester
        tester = FrameDetector.FrameDetector()