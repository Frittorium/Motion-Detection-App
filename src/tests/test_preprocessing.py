import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from preprocessing import preprocess


class TestPreprocessing(unittest.TestCase):
    def test_valid_bgr_frame(self):
        bgr = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        out = preprocess(bgr)
        self.assertEqual(out.shape, (config.FRAME_HEIGHT, config.FRAME_WIDTH))
        self.assertEqual(out.dtype, np.uint8)

    def test_resizes_to_processing_resolution(self):
        bgr = np.zeros((240, 320, 3), dtype=np.uint8)
        out = preprocess(bgr)
        self.assertEqual(out.shape, (config.FRAME_HEIGHT, config.FRAME_WIDTH))

    def test_invalid_inputs_return_none(self):
        self.assertIsNone(preprocess(None))
        self.assertIsNone(preprocess(np.empty((0, 0, 3), dtype=np.uint8)))
        self.assertIsNone(preprocess(np.zeros((480, 640, 4), dtype=np.uint8)))
        self.assertIsNone(preprocess("not a frame"))


if __name__ == "__main__":
    unittest.main()