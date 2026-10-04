# Motion Detection Application

A local Python application that captures video from the default camera, detects movement between consecutive frames, and displays the motion state on the live feed.

Version 1 does motion detection only. It does not detect, classify, or label objects.

## Features

- Live camera feed with a "Motion Detected" / "No Motion" overlay
- Frame-differencing motion detection with configurable thresholds
- Safe handling of camera failures and invalid frames
- Controlled shutdown that releases the camera and OpenCV windows
- Fully local: no frames are saved, recorded, or transmitted

## Requirements

- Python 3.8+
- A working webcam
- OpenCV and NumPy

## Installation

```
git clone https://github.com/Frittorium/motion_detection_app.git
cd motion_detection_app

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install opencv-python numpy
```

## Usage

```
python main.py
```

A window titled "Motion Detection" opens with the live feed. Press `q` with the window focused to exit.

If the camera does not open, set `CAMERA_INDEX = 1` in `config.py`. On macOS, grant your terminal camera access under System Settings > Privacy & Security > Camera.

## Configuration

All settings live in `config.py`.

| Setting | Default | Description |
|---|---|---|
| `CAMERA_INDEX` | `0` | Camera device index |
| `MOTION_THRESHOLD` | `25` | Per-pixel intensity difference (0-255) counted as changed |
| `MIN_MOTION_AREA` | `500` | Changed pixels required to report motion |
| `FRAME_WIDTH` / `FRAME_HEIGHT` | `640` / `480` | Processing resolution |
| `EXIT_KEY` | `"q"` | Key that exits the application |
| `DEBUG` | `False` | Shows motion area on screen and enables debug logs |
| `LOG_LEVEL` | `"INFO"` | Logging level |
| `WINDOW_NAME` | `"Motion Detection"` | Display window title |

Set `DEBUG = True` while tuning `MOTION_THRESHOLD` and `MIN_MOTION_AREA`.

## Project Structure

```
motion_detection_app/
├── main.py              # Entry point and application controller
├── camera.py            # Camera manager (sole owner of cv2.VideoCapture)
├── preprocessing.py     # Grayscale conversion and smoothing
├── motion_detector.py   # Frame-differencing motion detection
├── renderer.py          # Draws motion status on the frame
├── config.py            # Centralized configuration
├── logger.py            # Logging setup
└── tests/
    ├── test_motion_detector.py
    ├── test_preprocessing.py
    └── test_camera.py
```

## Testing

```
python -m unittest discover -s tests
```

Integration, end-to-end, fault, and performance tests require a physical camera and display and are performed manually.

## Privacy

All processing happens locally in memory. The application never writes frames or screenshots to disk, records video, or makes network connections. Logs contain diagnostic state only, never image data.