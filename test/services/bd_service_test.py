from unittest import TestCase
from app.services import BDService


class BdServiceTest(TestCase):
    service = BDService()

    def test_get(self):
        comet = self.service.get_comet_by_name("Ceres")
        print(comet)
        assert comet is not None
