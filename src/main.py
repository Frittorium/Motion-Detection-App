import sys
import time

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
        canvas = np.zeros((config.CAPTURE_HEIGHT, config.CAPTURE_WIDTH, 3), dtype=np.uint8)
        cv2.putText(canvas, message, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow(config.WINDOW_NAME, canvas)
        cv2.waitKey(2000)
    except Exception:
        pass  # Display not possible; stderr message already shown.


def run_processing_loop(camera: Camera) -> None:
    log = get_logger()
    detector = MotionDetector()
    
    consecutive_failures = 0
    reconnect_attempts = 0
    last_failure_log = 0.0
    fps_frames = 0
    fps_window_start = time.monotonic()

    while True:    ###
        frame = camera.read()
        if frame is None:
            consecutive_failures += 1
            now = time.monotonic()
            if now - last_failure_log >= config.READ_FAILURE_LOG_INTERVAL_S:
                log.warning("Frame read failure (%d consecutive)", consecutive_failures)
                last_failure_log = now

            if consecutive_failures >= config.MAX_CONSECUTIVE_READ_FAILURES:
                if reconnect_attempts >= config.MAX_RECONNECT_ATTEMPTS:
                    log.error("Camera read failed %d times; shutting down", consecutive_failures)
                    break
                reconnect_attempts += 1
                log.warning(
                    "Attempting camera reconnect (%d/%d)",
                    reconnect_attempts, config.MAX_RECONNECT_ATTEMPTS,
                )
                camera.release()
                camera.open()
                consecutive_failures = 0

            if exit_requested():
                break
            time.sleep(config.READ_RETRY_DELAY_S)
            continue

        consecutive_failures = 0
        reconnect_attempts = 0

        fps_frames += 1
        elapsed = time.monotonic() - fps_window_start
        if elapsed >= config.FPS_LOG_INTERVAL_S:
            log.info(
                "Delivered FPS: %.1f (requested %s)",
                fps_frames / elapsed, config.CAPTURE_FPS,
            )
            fps_frames = 0
            fps_window_start = time.monotonic()
        log.debug("Frame captured")

        if not is_valid_frame(frame):
            log.warning("Invalid frame")
            if exit_requested():
                break
            continue
        t_start = time.perf_counter()
        processed = preprocess(frame)
        if processed is None:
            log.warning("Invalid frame (preprocessing rejected)")
            if exit_requested():
                break
            continue

        result = detector.detect(processed)
        log.debug("Processing time: %.2f ms", (time.perf_counter() - t_start) * 1000)
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