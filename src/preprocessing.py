import cv2
import numpy as np

import config

_BLUR_KERNEL = (21, 21)


def is_valid_frame(frame) -> bool:
    return (
        isinstance(frame, np.ndarray)
        and frame.size > 0
        and frame.ndim in (2, 3)
    )


def preprocess(frame):
    """Return a grayscale, lightly smoothed frame, or None if input is invalid."""
    if not is_valid_frame(frame):
        return None

    if frame.ndim == 3:
        if frame.shape[2] != 3:
            return None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame

    if gray.shape != (config.FRAME_HEIGHT, config.FRAME_WIDTH):
        gray = cv2.resize(gray, (config.FRAME_WIDTH, config.FRAME_HEIGHT))

    return cv2.GaussianBlur(gray, _BLUR_KERNEL, 0)