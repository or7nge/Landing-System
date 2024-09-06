from config import *
import numpy as np
import cv2
from .directive import Directive


class FrameExtended(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def show_info(self, directive=Directive("NO ARUKO"), aruko0=None, aruko1=None):
        self.show_aruko(aruko0, (0, 0, 255))
        self.show_aruko(aruko1, (90, 90, 90))

        if aruko0:
            # draw the outline of the ArUco marker
            cv2.line(self, (0, 0), aruko0.topLeft, (255, 0, 0), 2)
            cv2.line(self, (FRAME_WIDTH - 1, 0), aruko0.topRight, (255, 0, 0), 2)
            cv2.line(self, (0, FRAME_WIDTH - 1), aruko0.bottomLeft, (255, 0, 0), 2)
            cv2.line(self, (FRAME_WIDTH - 1, FRAME_WIDTH - 1), aruko0.bottomRight, (255, 0, 0), 2)

            cv2.putText(self, f"DRONE ROTATION: {round(aruko0.get_drone_rotation(), 2)}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(self, f"DRONE HEIGHT: {round(aruko0.get_real_height(), 2)}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        self.update_directive(str(directive), directive.color())

    def show_aruko(self, aruko, color):
        if not aruko:
            return
        cv2.line(self, aruko.topLeft, aruko.topRight, color, 2)
        cv2.line(self, aruko.topRight, aruko.bottomRight, color, 2)
        cv2.line(self, aruko.bottomRight, aruko.bottomLeft, color, 2)
        cv2.line(self, aruko.bottomLeft, aruko.topLeft, color, 2)
        cv2.circle(self, aruko.get_center(), 6, color, -1)

    def update_directive(self, text, color):
        text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = FRAME_WIDTH // 2 - text_width // 2
        text_y = FRAME_WIDTH // 2 - DISTANCE_THRESHOLD - 10 - text_height // 2
        cv2.putText(self, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
