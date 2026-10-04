import cv2

import config
from logger import get_logger


class Camera:
    """Sole owner of cv2.VideoCapture."""

    def __init__(self):
        self._capture = None

    def open(self) -> bool:
        log = get_logger()
        try:
            self._capture = cv2.VideoCapture(config.CAMERA_INDEX)
            if not self._capture.isOpened():
                log.error("Camera unavailable (index %s)", config.CAMERA_INDEX)
                self.release()
                return False
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)
            self._capture.set(cv2.CAP_PROP_FPS, config.CAPTURE_FPS)

            actual_w = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = float(self._capture.get(cv2.CAP_PROP_FPS))
            log.info(
                "Camera initialized: requested %dx%d @ %s FPS, negotiated %dx%d @ %.1f FPS",
                config.CAPTURE_WIDTH, config.CAPTURE_HEIGHT, config.CAPTURE_FPS,
                actual_w, actual_h, actual_fps,
            )
            if (actual_w, actual_h) != (config.CAPTURE_WIDTH, config.CAPTURE_HEIGHT):
                log.warning("Camera resolution differs from the requested resolution")
            return True
        except Exception:
            log.exception("Camera unavailable")
            self.release()
            return False

    def read(self):
        """Return a frame, or None if the read failed."""
        if not self.is_open():
            return None
        ok, frame = self._capture.read()
        if not ok:
            return None
        return frame

    def is_open(self) -> bool:
        return self._capture is not None and self._capture.isOpened()

    def release(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None
            get_logger().debug("Resource release: camera")