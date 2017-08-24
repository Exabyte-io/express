from tests.unit import UnitTestBase
from express.properties.scalar.volume import Volume

VOLUME = {
    "units": "angstrom^3",
    "name": "volume",
    "value": 1
}


class VolumeTest(UnitTestBase):
    def setUp(self):
        super(VolumeTest, self).setUp()

    def tearDown(self):
        super(VolumeTest, self).setUp()

    def test_volume(self):
        property_ = Volume("volume", raw_data={"volume": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), VOLUME)
