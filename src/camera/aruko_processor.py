from config import *
import numpy as numpy
from .frame_extended import FrameExtended
from .aruko_detector import OrangeArucoDetector
from .detected_aruko import DetectedAruko
from .directive import Directive
from .aruko_queue import ArucoQueue
from .aby_queue import ABYQueue


class ArukoProcessor:
    def __init__(self, queue):
        self.queue = queue
        self.aruko_detector = OrangeArucoDetector()
        self.aruko_queue = (ArucoQueue(ARUKO_SMALL_WIDTH), ArucoQueue(ARUKO_BIG_WIDTH))
        self.current_aruko = "big"
        self.height_queue = ABYQueue(HEIGHT_QUEUE_SIZE)

    def add_frame(self, frame):
        frame = FrameExtended(frame)
        self.find_arukos(frame)
        small_aruko, big_aruko = (self.aruko_queue[0].get_prediction(), self.aruko_queue[1].get_prediction())

        if self.current_aruko == "small":
            if small_aruko:
                self.height_queue.add(small_aruko.get_real_height())
            elif big_aruko:
                self.height_queue.add(big_aruko.get_real_height())
            else:
                self.height_queue.add(None)
        elif self.current_aruko == "big":
            if big_aruko:
                self.height_queue.add(big_aruko.get_real_height())
            elif small_aruko:
                self.height_queue.add(small_aruko.get_real_height())
            else:
                self.height_queue.add(None)
        height = self.height_queue.get_prediction()

        current_directive = self.get_directive()
        self.queue.put(current_directive)

        if self.current_aruko == "small":
            frame.show_info(current_directive, height, small_aruko, big_aruko)
        else:
            frame.show_info(current_directive, height, big_aruko, small_aruko)
        return frame

    def get_directive(self):
        small_aruko, big_aruko = (self.aruko_queue[0].get_prediction(), self.aruko_queue[1].get_prediction())
        height = self.height_queue.get_prediction()
        if self.current_aruko == "big" and small_aruko and height < HEIGHT_BIG_TO_SMALL:
            self.current_aruko = "small"
        if self.current_aruko == "small" and big_aruko and height > HEIGHT_SMALL_TO_BIG:
            self.current_aruko = "big"
        if self.current_aruko == "small" and small_aruko:
            return self.directive_from_aruko(small_aruko)
        elif self.current_aruko == "big" and big_aruko:
            return self.directive_from_aruko(big_aruko)
        return Directive("NO ARUKO")

    def directive_from_aruko(self, aruko):
        deviation = aruko.get_aruko_deviation()
        drone_rotation = aruko.get_drone_rotation()
        front_rotation = aruko.get_front_rotation()
        aruco_pixel_width = aruko.get_aruco_pixel_width()

        if deviation < ARUKO_DEVIATION_THRESHOLD:
            if aruco_pixel_width > FRAME_WIDTH // 3 and abs(front_rotation) > FRONT_ROTATION_THRESHOLD:
                return Directive("ROTATE", int(front_rotation))
            return Directive("DESCEND")
        if abs(drone_rotation) > DRONE_ROTATION_THRESHOLD:
            return Directive("ROTATE", int(drone_rotation))
        return Directive("MOVE", int(aruko.get_real_distance()))

    def find_arukos(self, frame):
        arukos = self.aruko_detector.detectMarker(frame)
        for i in range(2):
            self.aruko_queue[i].add(arukos[i])
