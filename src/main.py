import sys

import cv2
import numpy as np

import config
from camera import Camera
from logger import initialize_logging, get_logger
from motion_detector import MotionDetector
from preprocessing import is_valid_frame, preprocess
from renderer import render


def exit_requested() -> bool:
    key = cv2.waitKey(1) & 0xFF
    return key == ord(config.EXIT_KEY)


def handle_camera_failure() -> None:
    message = "Camera unavailable"
    print(message, file=sys.stderr)
    try:
        canvas = np.zeros((config.FRAME_HEIGHT, config.FRAME_WIDTH, 3), dtype=np.uint8)
        cv2.putText(canvas, message, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow(config.WINDOW_NAME, canvas)
        cv2.waitKey(2000)
    except Exception:
        pass  # Display not possible; stderr message already shown.


def run_processing_loop(camera: Camera) -> None:
    log = get_logger()
    detector = MotionDetector()

    while True:
        frame = camera.read()
        if frame is None:
            log.warning("Frame read failure")
            if exit_requested():
                break
            continue
        log.debug("Frame captured")

        if not is_valid_frame(frame):
            log.warning("Invalid frame")
            if exit_requested():
                break
            continue

        processed = preprocess(frame)
        if processed is None:
            log.warning("Invalid frame (preprocessing rejected)")
            if exit_requested():
                break
            continue

        result = detector.detect(processed)
        output = render(frame, result)

        try:
            cv2.imshow(config.WINDOW_NAME, output)
        except cv2.error:
            log.error("Display failure", exc_info=True)
            break

        if exit_requested():
            break


def main() -> int:
    initialize_logging()
    log = get_logger()
    log.info("Application started")
    camera = Camera()
    exit_code = 0

    try:
        camera.open()

        if not camera.is_open():
            handle_camera_failure()
            exit_code = 1
            return exit_code

        run_processing_loop(camera)

    except Exception:
        log.exception("Unexpected application failure")
        exit_code = 1
    finally:
        camera.release()
        cv2.destroyAllWindows()
        log.info("Application shutdown")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())