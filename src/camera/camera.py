from config import *
import cv2
from .aruko_processor import ArukoProcessor
import time


class Camera:
    def __init__(self, queue):
        self.queue = queue
        self.video = cv2.VideoCapture(0)
        self.aruko_processor = ArukoProcessor(self.queue)

    def cut_frame(self, frame):
        global FRAME_WIDTH
        FRAME_WIDTH = min(frame.shape[:2])
        height, width, _ = frame.shape
        start_x = (width - FRAME_WIDTH) // 2
        start_y = (height - FRAME_WIDTH) // 2
        frame = frame[start_y: start_y + FRAME_WIDTH, start_x: start_x + FRAME_WIDTH]
        return frame

    def interpolate(self, frame, multiplier=1):
        height, width = frame.shape[:2]
        new_height = height * multiplier
        new_width = width * multiplier
        scaled_image = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        return scaled_image

    def camera_loop(self):
        while True:
            ret, frame = self.video.read()
            frame = self.cut_frame(frame)
            if ret is False:
                break

            extended_frame = self.aruko_processor.add_frame(frame)
            extended_frame = self.interpolate(extended_frame, 2)
            cv2.imshow("Image", extended_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        self.video.release()


def start_camera_loop(queue):
    camera = Camera(queue)
    camera.camera_loop()
