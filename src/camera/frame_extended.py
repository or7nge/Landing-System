from config import *
import numpy as numpy
import cv2
from .directive import Directive


class FrameExtended(numpy.ndarray):
    def __new__(cls, input_array):
        obj = numpy.asarray(input_array).view(cls)
        return obj

    def show_info(self, directive=Directive("NO ARUKO"), aruko0=None, aruko1=None, height=None):
        # Extend the frame to add a white field at the bottom
        extended_frame = cv2.copyMakeBorder(self, 0, 100, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))

        # Show ArUco markers
        self.show_aruko(aruko0, (0, 0, 255))
        self.show_aruko(aruko1, (90, 90, 90))

        if aruko0 is not None:
            # Draw the outline of the ArUco marker
            cv2.line(extended_frame, (0, 0), aruko0.topLeft, (255, 0, 0), 2)
            cv2.line(extended_frame, (FRAME_WIDTH - 1, 0), aruko0.topRight, (255, 0, 0), 2)
            cv2.line(extended_frame, (0, FRAME_WIDTH - 1), aruko0.bottomLeft, (255, 0, 0), 2)
            cv2.line(extended_frame, (FRAME_WIDTH - 1, FRAME_WIDTH - 1), aruko0.bottomRight, (255, 0, 0), 2)

            # Add text information
            cv2.putText(extended_frame, f"DRONE ROTATION: {round(aruko0.get_drone_rotation(), 2)}",
                        (10, FRAME_WIDTH + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            cv2.putText(extended_frame, f"DRONE HEIGHT: {round(height, 2)}",
                        (10, FRAME_WIDTH + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        # Update directive
        self.update_directive(str(directive), directive.color())

        # Return the extended frame
        return extended_frame

    def show_aruko(self, aruko, color):
        if aruko is None:
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
