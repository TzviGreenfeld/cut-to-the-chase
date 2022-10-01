import sys
from tools.frame_detector import FrameDetector, Frame
from tools.video_tools import Editor, Duration


def main(*args, **kwargs):
    file_name = args[0]
    editor = Editor(file_path=file_name)

    h, w = editor.h, editor.w
    frames = editor.get_frame_every_x_seconds(
        x=2, crop=(h//2, h, w//2, w), blackAndWhite=True)
    frames_dict = {f[0]: f[1] for f in frames}

    detector = FrameDetector(frames_dict)
    detector.detect()
    best = detector.get_best_results()

    for frame in sorted(best, key=lambda x: x.stamp):
        dur = 0
        if frame.text[0] == '1':
            dur = 60
        elif frame.text[0] == '2':
            dur = 120

        editor.add_subclip(int(frame.stamp), dur + 3)

    editor.output_concatenated_sub_clips(args[1])


if __name__ == "__main__":
    # call main with all arguments
    main(*sys.argv[1:])
