import unittest

from llm_input.audio_params_local import clamp_local_recording_params


class TestLocalAudioParams(unittest.TestCase):
    def test_defaults_ok(self):
        d, r, g = clamp_local_recording_params(5, 16000, 1)
        self.assertEqual((d, r, g), (5.0, 16000, 1.0))

    def test_rejects_huge_duration(self):
        with self.assertRaises(ValueError):
            clamp_local_recording_params(1e9, 16000, 1)

    def test_rejects_nan_gain(self):
        with self.assertRaises(ValueError):
            clamp_local_recording_params(5, 16000, float("nan"))

    def test_rejects_bad_rate(self):
        with self.assertRaises(ValueError):
            clamp_local_recording_params(5, 100, 1)


if __name__ == "__main__":
    unittest.main()
