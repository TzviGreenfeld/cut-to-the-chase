import moviepy.editor as mpy
import atexit
from pytube import YouTube


class Editor:
    def download(self, youtube_url):
        """
        download video from youtube
        :param youtube_url: video link
        :return:
        """
        #test if valid url
        video = YouTube(youtube_url)
        video.streams.filter(file_extension="mp4").order_by("fps").get_highest_resolution.download()
        self.original_file = open(video.title + ".mp4", "r")

    def __init__(self, youtube_url=None, file_path=None):
        if youtube_url is not None:
            self.download(youtube_url)

        if file_path is not None:
            self.original_file = open(file_path, "r")

        self.clips = []
        self.VideoFileClip = mpy.VideoFileClip(self.original_file)
        self.fps = self.VideoFileClip.fps
        self.duration = self.VideoFileClip.duration
        self.w = self.VideoFileClip.w
        self.h = self.VideoFileClip.h

    @atexit.register
    def close(self):
        if self.original_file is not None:
            self.original_file.close()

    def grid(self, i, j):
        """
        break photo area to an ixj grid
        from (0,0) to (i-1,j-1)
        :return: list of tuples ( (top_left_x, top_left_y) , (bottom_right_x, bottom_right_y) )
        """
        w_interval = self.w // i
        h_interval = self.h // j

        grid_ = [[((w_interval * (x - 1), h_interval * (y - 1)), (w_interval * (x), h_interval * (y)))
                  for x in range(1, i + 1)] for y in range(1, j + 1)]

        return grid_

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

    def output_concatenated_subClips(self, output_file_name):
        """
        concatenate sub clips to one file
        :param output_file_name: name, should end with some video file suffix
        :return: true if succeeded, false otherwise
        """
        final_clip = mpy.concatenate_videoclips(self.clips)
        try:
            final_clip.write_videofile(output_file_name)
        except Exception as e:
            print(e)
            return False

        return True


if __name__ == '__main__':
    print("hi")
