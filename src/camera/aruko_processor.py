from config import *
import numpy as np
from .frame_extended import FrameExtended
from .aruko_detector import OrangeArucoDetector
from .detected_aruko import DetectedAruko
from .directive import Directive
from .aruko_queue import ArucoQueue


class ArukoProcessor:
    def __init__(self, queue):
        self.queue = queue
        self.aruko_detector = OrangeArucoDetector()
        self.aruko_queue = (ArucoQueue(ARUKO_SMALL_WIDTH), ArucoQueue(ARUKO_BIG_WIDTH))
        self.selected_aruko = 0

    def add_frame(self, frame):
        frame = FrameExtended(frame)
        self.find_arukos(frame)
        current_directive = self.get_directive()
        self.queue.put(current_directive)

        if self.selected_aruko == "small":
            frame.show_info(
                current_directive,
                self.aruko_queue[0].average_aruko,
                self.aruko_queue[1].average_aruko
            )
        elif self.selected_aruko == "big":
            frame.show_info(
                current_directive,
                self.aruko_queue[1].average_aruko,
                self.aruko_queue[0].average_aruko
            )
        else:
            frame.show_info(current_directive)
        return frame

    def get_directive(self):
        small_aruko, big_aruko = (self.aruko_queue[0].average_aruko, self.aruko_queue[1].average_aruko)
        if small_aruko and (not big_aruko or self.selected_aruko == "small") and small_aruko.get_real_distance() < SWITCH_ARUKO_HEIGHT_MAX:
            self.selected_aruko = "small"
            return self.directive_from_aruko(small_aruko)
        elif big_aruko:
            self.selected_aruko = "big"
            return self.directive_from_aruko(big_aruko)
        self.selected_aruko = None
        return Directive("NO ARUKO")

    def directive_from_aruko(self, aruko):
        distance = aruko.get_pixel_distance()
        drone_rotation = aruko.get_drone_rotation()
        front_rotation = aruko.get_front_rotation()
        aruco_pixel_width = aruko.get_aruco_pixel_width()

        if distance < DISTANCE_THRESHOLD:
            if aruco_pixel_width > FRAME_WIDTH // 3 and abs(front_rotation) > FRONT_ROTATION_THRESHOLD:
                return Directive("ROTATE", int(front_rotation))
            return Directive("DESCEND")
        if abs(drone_rotation) > DRONE_ROTATION_THRESHOLD:
            return Directive("ROTATE", int(drone_rotation))
        return Directive("MOVE", int(aruko.get_real_distance()))

    def find_arukos(self, frame):
        arukos = self.aruko_detector.detectMarker(frame)
        self.aruko_queue[0].add(arukos[0])
        self.aruko_queue[1].add(arukos[1])
