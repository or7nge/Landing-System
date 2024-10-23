from config import *
from .detected_aruko import DetectedAruko
from .aby_queue import ABYQueue
from collections import deque
import numpy
import time


class ArucoQueue:
    def __init__(self, aruko_width):
        self.aruko_width = aruko_width
        self.queues = numpy.array([[ABYQueue(ARUKO_QUEUE_SIZE) for _ in range(2)] for _ in range(4)])

    def add(self, aruco):
        for i in range(4):
            for j in range(2):
                if aruco is None:
                    self.queues[i][j].add(None)
                else:
                    self.queues[i][j].add(aruco[i][j])
        # numpy.vectorize(lambda queue, cord: queue.add(cord))(self.queues, aruco)

    def get_prediction(self):
        prediction = numpy.array([[self.queues[i][j].get_prediction() for j in range(2)]
                                 for i in range(4)])
        if prediction[0][0] is None:
            return None
        else:
            return DetectedAruko(numpy.round(prediction).astype(int), self.aruko_width)

    def get_speed(self):
        if self.queues[0][0].get_prediction() is None:
            return None
        else:
            return
