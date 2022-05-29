from videoTools import Editor
import os
import cv2


def init():
    tester = Editor(file_path="test.mp4")
    print(tester)
    # try:
    #     tester = Editor("test.mp4")
    # except Exception as e:
    #     print("init Error: ", e)


def test_download():
    name, url = "Countdown 5 seconds timer", "https://www.youtube.com/watch?v=icPHcK_cCF4"
    if os.path.exists(name + ".mp4"):
        os.remove(name + ".mp4")
    try:
        yt_vid = Editor(url)
    except Exception as e:
        print("test_download Error:", e)
    return os.path.exists(name + ".mp4")


def test_grid(i, j):
    pass


def test_add_subclip(start_time, duration):
    pass


def test_output_concatenated_sub_clips(output_file_name):
    pass


def test_gat_frame_every_x_seconds(x, path):
    pass


if __name__ == '__main__':
    # print("test_download:", test_download())
    # print("test_grid:", test_grid())
    init()
