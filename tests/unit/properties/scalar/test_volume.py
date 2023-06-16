from tests.unit import UnitTestBase
from express.properties.scalar.volume import Volume

VOLUME = {"units": "angstrom^3", "name": "volume", "value": 1}


class VolumeTest(UnitTestBase):
    def setUp(self):
        super(VolumeTest, self).setUp()

    def tearDown(self):
        super(VolumeTest, self).setUp()

    def test_volume(self):
        parser = self.get_mocked_parser("volume", 1)
        property_ = Volume("volume", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), VOLUME)
