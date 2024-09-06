from config import *
from .detected_aruko import DetectedAruko
from collections import deque
import numpy


class ArucoQueue:
    def __init__(self, aruko_width):
        self.aruko_width = aruko_width
        self.queue = deque(maxlen=ARUKO_QUEUE_SIZE)
        self.average_aruko = None

    def add(self, aruco):
        self.queue.append(aruco)
        self.update_average()

    def get(self):
        return self.queue

    def update_average(self):
        if not self.queue:
            return None
        aruco_queue_cleared = []
        weights = []
        for i in range(len(self.queue)):
            if self.queue[i] is not None:
                aruco_queue_cleared.append(self.queue[i])
                weights.append(i + 1)
        if not aruco_queue_cleared:
            self.average_aruko = None
        else:
            self.average_aruko = DetectedAruko(numpy.average(
                aruco_queue_cleared, axis=0, weights=weights), self.aruko_width)
