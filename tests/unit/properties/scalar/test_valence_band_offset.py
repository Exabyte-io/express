from tests.unit import UnitTestBase
from express.properties.scalar.scalar_property_context import ScalarPropertyFromContext

VALENCE_BAND_OFFSET = {"units": "eV", "name": "valence_band_offset", "value": 1}


class ValenceBandOffsetTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_valence_band_offset(self):
        parser = self.get_mocked_parser("valence_band_offset", 1)  # noqa : F841
        property_ = ScalarPropertyFromContext("valence_band_offset", None, value=1)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), VALENCE_BAND_OFFSET)
