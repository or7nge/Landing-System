from config import *
import cv2
from .detected_aruko import DetectedAruko
import numpy


class OrangeArucoDetector(cv2.aruco.ArucoDetector):
    def __init__(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = cv2.aruco.DetectorParameters()
        super().__init__(self.dictionary, self.parameters)

    def detectMarker(self, image):
        (corners, ids, rejected) = self.detectMarkers(image)
        if not corners:
            return (None, None)
        ids = ids.flatten()
        return (
            self.find_aruko(corners, ids, ARUKO_SMALL_ID),
            self.find_aruko(corners, ids, ARUKO_BIG_ID),
        )

    def find_aruko(self, corners, ids, id):
        if id not in ids:
            return None
        else:
            return corners[numpy.where(ids == id)[0][0]][0]
