from unittest import TestCase
from app.config import Config


class ConfigTest(TestCase):
    config = Config()

    def test_get(self):
        assert self.config["bot"]["api"] is not None
