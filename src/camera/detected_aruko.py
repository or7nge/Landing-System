from config import *
import numpy as numpy


class DetectedAruko:
    def __init__(self, corners, aruko_wdith):
        self.corners = corners
        self.aruko_width = aruko_wdith
        self.drone_center = numpy.array([FRAME_WIDTH // 2, FRAME_WIDTH // 2])
        self.topLeft = self.corners[0].astype(int)
        self.topRight = self.corners[1].astype(int)
        self.bottomRight = self.corners[2].astype(int)
        self.bottomLeft = self.corners[3].astype(int)

    def get_center(self):
        return numpy.mean(self.corners, axis=0).astype(int)

    def get_pixel_distance(self):
        center = self.get_center()
        distance = numpy.linalg.norm(center - self.drone_center)
        return distance

    def get_real_distance(self):
        return self.get_pixel_distance() / self.get_aruco_pixel_width() * self.aruko_width

    def get_drone_rotation(self):
        center = self.get_center()
        angle = numpy.arctan2(center[0] - self.drone_center[0], self.drone_center[1] - center[1])
        angle = numpy.degrees(angle)
        return angle

    def get_front_rotation(self):
        angle = numpy.arctan2(self.topRight[1] - self.topLeft[1], self.topRight[0] - self.topLeft[0])
        angle = numpy.degrees(angle)
        return angle

    def get_aruco_pixel_width(self):
        return numpy.linalg.norm(self.topLeft - self.topRight)

    def get_frame_real_width(self):
        return FRAME_WIDTH * self.aruko_width / self.get_aruco_pixel_width()

    def get_aruko_deviation(self):
        angle = numpy.arctan2(self.get_real_distance(), self.get_real_height())
        angle = numpy.degrees(angle)
        return angle

    def get_real_height(self):
        frame_real_width = self.get_frame_real_width()
        return (frame_real_width / 2) / numpy.tan(numpy.radians(CAMERA_ANGLE / 2))
