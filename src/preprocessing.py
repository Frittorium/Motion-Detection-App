import cv2
import numpy as np

import config

_BLUR_KERNEL = (config.BLUR_KERNEL_SIZE, config.BLUR_KERNEL_SIZE)
_INTERPOLATION = getattr(cv2, "INTER_" + config.RESIZE_INTERPOLATION)

if config.BLUR_KERNEL_SIZE < 1 or config.BLUR_KERNEL_SIZE % 2 == 0:
    raise ValueError("BLUR_KERNEL_SIZE must be a positive odd integer")

###
def is_valid_frame(frame) -> bool:
    """Contract: non-empty uint8 ndarray, either (H, W) gray or (H, W, 3) BGR."""
    if not isinstance(frame, np.ndarray) or frame.size == 0:
        return False
    if frame.dtype != np.uint8:
        return False
    if frame.ndim == 2:
        return True
    return frame.ndim == 3 and frame.shape[2] == 3
###


def preprocess(frame):
    """Return a grayscale, lightly smoothed frame, or None if input is invalid."""
    if not is_valid_frame(frame):
        return None

    size = (config.PROCESSING_WIDTH, config.PROCESSING_HEIGHT)
    needs_resize = frame.shape[:2] != (config.PROCESSING_HEIGHT, config.PROCESSING_WIDTH)

    if config.RESIZE_BEFORE_GRAYSCALE and needs_resize:
        frame = cv2.resize(frame, size, interpolation=_INTERPOLATION)
        needs_resize = False

    if frame.ndim == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame

    if needs_resize:
        gray = cv2.resize(gray, size, interpolation=_INTERPOLATION)

    return cv2.GaussianBlur(gray, _BLUR_KERNEL, 0)