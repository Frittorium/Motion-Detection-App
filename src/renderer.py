import cv2

import config

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_GREEN = (0, 255, 0)
_WHITE = (255, 255, 255)


def render(frame, motion_result):
    """Draw the motion status on the frame and return it."""
    if motion_result.motion_detected:
        text, color = "Motion Detected", _GREEN
    else:
        text, color = "No Motion", _WHITE

    cv2.putText(frame, text, (10, 30), _FONT, 0.9, color, 2, cv2.LINE_AA)

    if config.DEBUG:
        cv2.putText(
            frame,
            f"Area: {motion_result.motion_area}",
            (10, 60), _FONT, 0.6, color, 1, cv2.LINE_AA,
        )
    return frame