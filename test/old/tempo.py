import cv2
import numpy
import numpy as np


def locate_in_frame(template, img, expected_res):
    h, w = template.shape
    # methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]
    methods = [cv2.TM_CCOEFF_NORMED]
    # methods = [cv2.TM_CCOEFF]

    for idx, method in enumerate(methods):
        img2 = img.copy()
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # location = max_loc
        threshold = 0.9
        loc = np.where(result >= threshold)
        location = max_loc
        """
        use this soruce for threshold:
        https://stackoverflow.com/questions/36040630/how-to-interpret-matchtemplate-output-opencv-python
        """

        if loc is not None:
            print(expected_res)
            # bottom_right = (loc[0] + w, loc[1] + h)
            # cv2.rectangle(img2, loc, bottom_right, 255, 5)
            # cv2.imshow(str(idx), img2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        # bottom_right = (location[0] + w, location[1] + h)
        # cv2.rectangle(img2, location, bottom_right, 255, 5)
        # cv2.imshow(str(idx), img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    template_path = r"D:\code\chaser\test\US\1_min.png"
    template = cv2.imread(template_path, 0)
    # simple test cases
    frame0 = cv2.imread(r"D:\code\chaser\test\US\FALSE0.png", 0)
    frame1 = cv2.imread(r"D:\code\chaser\test\US\FALSE1.png", 0)
    frame2 = cv2.imread(r"D:\code\chaser\test\US\TRUE0.png", 0)
    frame3 = cv2.imread(r"D:\code\chaser\test\US\TRUE1.png", 0)
    frame4 = cv2.imread(r"D:\code\chaser\test\US\FALSE2.png", 0)
    frame5 = cv2.imread(r"D:\code\chaser\test\US\FALSE3.png", 0)
    frames = [(frame0, False), (frame1, False), (frame2, True), (frame3, True), (frame4, False), (frame5, False)]

    # actual test
    vid_path = r"D:\code\chaser\test\US\The.Chase.US.S02E17.720p.WEB.h264-KOGi.mkv"
    # cap = cv2.VideoCapture(vid_path)
    for frame in frames:
        locate_in_frame(template, *frame)
    # i = 0
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     i += 1
    #     if i % 60 == 0:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         locate_in_frame(img, frame)


