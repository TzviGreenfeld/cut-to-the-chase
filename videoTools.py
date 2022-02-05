import moviepy as mpy


class Editor:
    def __init__(self, youtube_URL=None, file_path=None):
        if youtube_URL is not None:
            # download video
            pass
        if file_path is not None:
            self.original_file = open(file_path, "r")

        def close():
            if self.original_file is not None:
                self.original_file.close()


if __name__ == '__main__':
    print("hi")
