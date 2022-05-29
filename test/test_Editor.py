from videoTools import Editor
import os
import unittest


class TestEditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global tester
        tester = Editor(file_path="test.mp4")

    def test_download(self):
        name, url = "Countdown 5 seconds timer", "https://www.youtube.com/watch?v=icPHcK_cCF4"
        if os.path.exists(name + ".mp4"):
            os.remove(name + ".mp4")
        try:
            yt_vid = Editor(url)
        except Exception as e:
            print("test_download Error:", e)
        self.assertTrue(os.path.exists(name + ".mp4"))

    def test_grid(self):
        # im = tester.VideoFileClip.get_frame(1)
        # cv2.imshow("full", im)
        # for i in range(4):
        #     for j in range(4):
        #         grid = tester.grid(4, 4, i, j)
        #         cv2.imshow(f"image{i},{j}", im[grid[0]: grid[1], grid[2]: grid[3]])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        i, j = 4, 4
        grid = tester.grid(i, j, 3, 3)
        est_h, est_w = grid[1], grid[3]  # TODO: isnt it backwards?

        self.assertTrue(abs(est_h - tester.h) + abs(est_w - tester.w) < 10)

    def test_add_subclip(self):
        first = len(tester.clips)
        tester.add_subclip((0, 1), (0, 2))
        self.assertTrue(len(tester.clips) == first + 1)

    def test_output_concatenated_sub_clips(self):
        def rm(filename):
            try:
                os.remove(filename)
                return True
            except:
                return False

        while len(tester.clips) > 0:
            tester.clips.pop()
        out_name = "testConcat.mp4"
        tester.add_subclip((0, 1), (0, 1))
        tester.add_subclip((0, 2), (0, 1.5))
        tester.output_concatenated_sub_clips(out_name)

        self.assertTrue(os.path.exists(out_name) and abs(Editor(file_path=out_name).duration - 2.5) < 0.05 and rm(out_name))

    # def test_gat_frame_every_x_seconds(self, x, path):
    #     pass

