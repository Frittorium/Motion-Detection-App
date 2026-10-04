from dataclasses import dataclass

import cv2
import numpy as np

import config
from logger import get_logger


@dataclass
class MotionResult:
    motion_detected: bool
    motion_area: int


class MotionDetector:
    def __init__(self, threshold=None, min_area=None):
        self._threshold = config.MOTION_THRESHOLD if threshold is None else threshold
        self._min_area = config.MIN_MOTION_AREA if min_area is None else min_area
        self._previous_frame = None

    @staticmethod
    def _is_valid(frame) -> bool:
        return isinstance(frame, np.ndarray) and frame.size > 0 and frame.ndim == 2

    def detect(self, frame) -> MotionResult:
        log = get_logger()

        # Invalid data is rejected and never overwrites the baseline.
        if not self._is_valid(frame):
            log.debug("Motion calculation skipped: invalid frame")
            return MotionResult(False, 0)

        # First valid frame (or a size change) establishes the baseline.
        if self._previous_frame is None or self._previous_frame.shape != frame.shape:
            self._previous_frame = frame
            return MotionResult(False, 0)

        diff = cv2.absdiff(self._previous_frame, frame)
        _, thresh = cv2.threshold(diff, self._threshold, 255, cv2.THRESH_BINARY)
        area = int(cv2.countNonZero(thresh))
        detected = area >= self._min_area

        log.debug("Motion area: %d", area)
        log.debug("Motion detected" if detected else "Motion not detected")

        self._previous_frame = frame
        return MotionResult(detected, area)