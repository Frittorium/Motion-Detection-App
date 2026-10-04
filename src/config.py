CAMERA_INDEX = 0

MOTION_THRESHOLD = 20      # per-pixel intensity difference (0-255)
MIN_MOTION_AREA = 500      # changed pixels required to count as motion

CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
CAPTURE_FPS = 30

# 640x480 vs 320x240.
PROCESSING_WIDTH = 320
PROCESSING_HEIGHT = 240

BLUR_KERNEL_SIZE = 5          # positive odd integer: try 5, 9, 21
RESIZE_BEFORE_GRAYSCALE = True    # True = resize first, then convert to gray
RESIZE_INTERPOLATION = "LINEAR"    # "LINEAR", "AREA", "NEAREST", "CUBIC"

MAX_CONSECUTIVE_READ_FAILURES = 30
READ_RETRY_DELAY_S = 0.05
READ_FAILURE_LOG_INTERVAL_S = 5.0
MAX_RECONNECT_ATTEMPTS = 3         # 0 = exit cleanly without reconnecting

FPS_LOG_INTERVAL_S = 5.0

EXIT_KEY = "q"

DEBUG = False
LOG_LEVEL = "INFO"
WINDOW_NAME = "Motion Detection"