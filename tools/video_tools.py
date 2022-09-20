import moviepy.editor as mpy
import numpy as np
from pytube import YouTube
from moviepy.editor import *

class Duration:
    def __init__(self, duration):
        self.hours = (duration / 3600)
        self.mins = (duration % 3600) / 60
        self.secs = (duration % 60)


class Editor:
    def __init__(self, youtube_url=None, file_path=None):
        self.original_file = None
        self.youtube_url = youtube_url
        self.file_path = file_path
        if youtube_url is not None:
            self.download(youtube_url)

        if file_path is not None:
            self.original_file = open(file_path, "r")

        self.clips = []
        self.VideoFileClip = mpy.VideoFileClip(
            self.original_file.name)  # TODO: do i really need to open?
        self.fps = self.VideoFileClip.fps
        self.duration = Duration(self.VideoFileClip.duration)
        self.w = self.VideoFileClip.w
        self.h = self.VideoFileClip.h

    def __del__(self):
        if self.original_file is not None:
            self.original_file.close()

    def __str__(self):
        out = ""
        out += "from URL: " + \
            (self.youtube_url if self.youtube_url is not None else "NO")
        out += "\nfrom file: " + \
            (self.file_path if self.file_path is not None else "NO")
        out += "\nduration: " + str(self.duration)
        out += "\nfps: " + str(self.fps)
        out += "\nclips: " + str(len(self.clips))
        out += "\nh, w: " + str(self.h) + "x" + str(self.w)
        return out

    def download(self, youtube_url):
        """
        download video from youtube
        :param youtube_url: video link
        :return:
        """
        # TODO: fix this function!
        # test if valid url
        video = YouTube(youtube_url)
        # for s in video.streams.filter(file_extension="mp4"):
        #     print(s)
        # video.streams.filter(file_extension="mp4").order_by("fps").get_highest_resolution.download()
        stream = video.streams.filter(
            file_extension="mp4").get_highest_resolution()
        # print(stream)
        stream.download()
        self.original_file = open(video.title + ".mp4", "r")
 

    def add_subclip(self, start_time, duration):
        """
        append subClip to self.clips
        :param start_time: first timestamp of subclip in (min, sec)
        :param duration: length of clip in (min, sec)
        :return:
        """
        # test if time in range
        end_time = (start_time[0] + duration[0], start_time[1] + duration[1])
        sub_clip = self.VideoFileClip.subclip(start_time, end_time)
        self.clips.append(sub_clip)

    def output_concatenated_sub_clips(self, output_file_name):
        """
        concatenate sub clips to one file
        :param output_file_name: name, should end with some video file suffix
        :return: true if succeeded, false otherwise
        """
        final_clip = mpy.concatenate_videoclips(self.clips)
        try:
            final_clip.write_videofile(output_file_name, codec="libx264")
        except Exception as e:
            print(e)
            return False

        return True

    def get_frame_every_x_seconds(self, x, crop=None, blackAndWhite=False):
        """
        get frame every x seconds
        :param x: seconds
        :param crop: tuple of (y1, y2, x1, x2)
        :param blackAndWhite: if true, convert to black and white
        :return: list of frames where frames[i][0] is the timestamp and frames[i][1] is the frame

        """
        clip = self.VideoFileClip
        if crop:
            clip = clip.crop(y1=crop[0], y2=crop[1], x1=crop[2], x2=crop[3])
        if blackAndWhite:
            clip = clip.fx(vfx.blackwhite)
        # detector is using {time:frame} and here we are using [time, frame]
        return clip.iter_frames(fps=(1 / x), with_times=True, dtype="uint8")
