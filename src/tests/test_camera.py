import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera import Camera


class TestCamera(unittest.TestCase):
    @patch("camera.cv2.VideoCapture")
    def test_open_success(self, mock_capture):
        mock_capture.return_value.isOpened.return_value = True
        cam = Camera()
        self.assertTrue(cam.open())
        self.assertTrue(cam.is_open())

    @patch("camera.cv2.VideoCapture")
    def test_open_failure_releases(self, mock_capture):
        cap = MagicMock()
        cap.isOpened.return_value = False
        mock_capture.return_value = cap
        cam = Camera()
        self.assertFalse(cam.open())
        self.assertFalse(cam.is_open())
        cap.release.assert_called_once()

    @patch("camera.cv2.VideoCapture")
    def test_read_failure_returns_none(self, mock_capture):
        cap = mock_capture.return_value
        cap.isOpened.return_value = True
        cap.read.return_value = (False, None)
        cam = Camera()
        cam.open()
        self.assertIsNone(cam.read())

    def test_read_when_closed_returns_none(self):
        self.assertIsNone(Camera().read())

    @patch("camera.cv2.VideoCapture")
    def test_release_is_idempotent(self, mock_capture):
        cap = mock_capture.return_value
        cap.isOpened.return_value = True
        cam = Camera()
        cam.open()
        cam.release()
        cam.release()
        cap.release.assert_called_once()
        self.assertFalse(cam.is_open())


if __name__ == "__main__":
    unittest.main()