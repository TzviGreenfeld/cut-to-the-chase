import moviepy.editor as mpy
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

    def grid(self, i, j, x, y):
        """
        break photo area to an ixj grid
        from (0,0) to (i-1,j-1)
        and return the x,y section
        :return: list of tuples ( (top_left_x, top_left_y) , (bottom_right_x, bottom_right_y) )
        """
        w_interval = self.w // i
        h_interval = self.h // j
        # img[y:y + h, x:x + w]
        if (x + 1) * i <= self.w and (y + 1) * j <= self.h:
            return (y * h_interval, (y + 1) * h_interval, x * w_interval, (x + 1) * w_interval)
 

    def add_subclip(self, start_time, duration):
        """
        append subClip to self. clips
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

    def get_frame_every_x_seconds(self, fps, grid=None, blackAndWhite=False):
        clip = self.VideoFileClip
        if grid:
            clip = clip.crop(y1=grid[0], y2=grid[1], x1=grid[2], x2=grid[3])
        if blackAndWhite:
            clip = clip.fx(vfx.blackwhite)

        clip.write_images_sequence(nameformat='frame%01d.png', fps=fps)
