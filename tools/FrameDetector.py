import cv2
import pytesseract


class FrameDetector:
    def __init__(self, frames):
        self.frames = frames

    def __str__(self):
        return "frames: " + str(len(self.frames))

    def show_frames(self):
        for idx, f in enumerate(self.frames):
            cv2.imshow(f"frame{idx}", f)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def find_digits(self):
        gray = self.frames[0]
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (120, 400))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        im2 = gray.copy()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.imshow("im2", im2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            print(text)


if __name__ == '__main__':
    frames = [cv2.imread("../test/bad.png", cv2.IMREAD_GRAYSCALE),
              cv2.imread("../test/good1.png", cv2.IMREAD_GRAYSCALE),
              cv2.imread("../test/good2.png", cv2.IMREAD_GRAYSCALE)]

    tester = FrameDetector(frames)
    tester.find_digits()
