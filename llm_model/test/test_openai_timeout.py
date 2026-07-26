import unittest

from llm_model.openai_timeout import clamp_openai_request_timeout


class TestOpenAITimeout(unittest.TestCase):
    def test_default_none(self):
        self.assertEqual(clamp_openai_request_timeout(None), 30.0)

    def test_clamp_high(self):
        self.assertEqual(clamp_openai_request_timeout(9999), 120.0)

    def test_clamp_low(self):
        self.assertEqual(clamp_openai_request_timeout(0), 1.0)

    def test_nan(self):
        self.assertEqual(clamp_openai_request_timeout(float("nan")), 30.0)

    def test_ok(self):
        self.assertEqual(clamp_openai_request_timeout(45), 45.0)


if __name__ == "__main__":
    unittest.main()
