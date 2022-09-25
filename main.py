from tools.frame_detector import FrameDetector, Frame
from tools.video_tools import Editor, Duration

if __name__ == "__main__":
    file_name = "test/samples/sample_episode.mp4"
    editor = Editor(file_path=file_name)
    
    h, w = editor.h, editor.w
    frames = editor.get_frame_every_x_seconds(x=2, crop=(h//2, h, w//2, w), blackAndWhite=True)
    frames_dict = {f[0]: f[1] for f in frames}
    
    detector = FrameDetector(frames_dict)
    detector.detect()
    best = detector.get_best_results()

    for frame in sorted(best, key=lambda x: x.stamp):
        editor.add_subclip(frame.stamp, frame.stamp + 60)
    editor.output_concatenated_sub_clips("test/samples/sample_episode_output.mp4")
        