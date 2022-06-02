import unittest

from tools import FrameDetector


class TestEditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global tester
        tester = FrameDetector.FrameDetector()
