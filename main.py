import sys
from tools import Editor, FrameDetector


def main(*args, **kwargs):
    file_name = args[0]
    editor = Editor(file_path=file_name)

    h, w = editor.h, editor.w
    # get frames of the right lower corner of the video in black and white
    frames = editor.get_frame_every_x_seconds(
        x=2, crop=(h//2, h, w//2, w), blackAndWhite=True)
    
    # from list iterator to dict, because this is what FrameDetector expects. TODO: change FrameDetector to accept iterators
    frames_dict = {f[0]: f[1] for f in frames}

    detector = FrameDetector(frames_dict)
    detector.detect()
    best = detector.get_best_results()

    for frame in sorted(best, key=lambda x: x.stamp):
        dur = 0
        if frame.text[0] == '1': # one minute timer
            dur = 60
        elif frame.text[0] == '2': # two minute timer
            dur = 120

        editor.add_subclip(int(frame.stamp), dur + 3)

    editor.output_concatenated_sub_clips(args[1])


if __name__ == "__main__":
    main(*sys.argv[1:])
