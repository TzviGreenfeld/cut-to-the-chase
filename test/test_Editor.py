from cgi import test
from videoTools import Editor
import unittest


class TestEditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.editor = Editor(youtube_url="https://www.youtube.com/watch?v=M5DeixPDL5k")

    def test_download(self):
        pass

    # def test_close(self):
    #     pass

    # def test_grid(self):
    #     pass

    # def test_add_subclip(self):
    #     pass

    # def test_output_concatenated_subClips(self):
    #     pass


if __name__ == '__main__':
    # unittest.main()
     Editor(youtube_url="https://www.youtube.com/watch?v=M5DeixPDL5k")
     print("hi")