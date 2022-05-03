import cv2
import numpy
import numpy as np


def locate_in_frame(template, img):
    h, w = template.shape
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]

    for idx, method in enumerate(methods):
        img2 = img.copy()
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val) # using max_val for threshold
        location = max_loc
        """
        use this soruce for threshold:
        https://stackoverflow.com/questions/36040630/how-to-interpret-matchtemplate-output-opencv-python
        """
        if max_val > 0.7:
            bottom_right = (location[0] + w, location[1] + h)
            cv2.rectangle(img2, location, bottom_right, 255, 5)
            cv2.imshow(str(idx), img2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    template_path = r"D:\code\chaser\test\US\1_min.png"
    template = cv2.imread(template_path, 0)
    # simple test cases
    frame0 = cv2.imread(r"D:\code\chaser\test\US\FALSE0.png", 0)
    frame1 = cv2.imread(r"D:\code\chaser\test\US\FALSE1.png", 0)
    frame2 = cv2.imread(r"D:\code\chaser\test\US\TRUE0.png", 0)
    frame3 = cv2.imread(r"D:\code\chaser\test\US\TRUE1.png", 0)
    frames = [frame0, frame1, frame2, frame3]

    # actual test
    vid_path = r"D:\code\chaser\test\US\The.Chase.US.S02E17.720p.WEB.h264-KOGi.mkv"
    # cap = cv2.VideoCapture(vid_path)
    for frame in frames:
        locate_in_frame(template, frame)
    # i = 0
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     i += 1
    #     if i % 60 == 0:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         locate_in_frame(img, frame)


# max_val
# false first method
# 12437787.0
# 6926610.5
# true first method
# 13567272.0
# 13493496.0

# false second method
# 0.3492107093334198
# 0.26925957202911377
# true second method
# 0.39505869150161743
# 0.3743186593055725

