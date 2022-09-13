import cv2
import os
os.chdir("/home/tzvigr/chaser/test/samples")
video_name = "./sample_episode.mp4"
vidcap = cv2.VideoCapture(video_name)
success,image = vidcap.read()

fps = vidcap.get(cv2.CAP_PROP_FPS)
# print(fps)
h, w, _ = image.shape
count = 0
while success:
    if count % 2*fps == 0: # every 2 seconds
        # convert image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("./normal/frame%d.jpg" % count, image)  
        cv2.imwrite("./medium/frame%d.jpg" % count, image[h//2:h, w//2:w])  
        cv2.imwrite("./small/frame%d.jpg" % count, image[3*(h//4):h, 2*(w//4):3*(w//4)])  
        cv2.imwrite("./tiny/frame%d.jpg" % count, image[int(6.5*(h/8)):int(7.5*(h/8)), 5*(w//8):6*(w//8)])  
        
    success,image = vidcap.read()
    # print('Read a new frame: ', success)
    count += 1