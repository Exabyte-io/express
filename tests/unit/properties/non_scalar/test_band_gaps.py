from tests.unit import UnitTestBase
from express.properties.non_scalar.bandgaps import BandGaps
from tests.unit.properties.raw_data import BAND_GAPS_RAW_DATA

BAND_GAPS = {
    "values": [
        {
            "units": "eV",
            "kpointConduction": [
                0.0,
                0.0,
                0.0
            ],
            "type": "direct",
            "value": 2.4420081600000003,
            "kpointValence": [
                0.0,
                0.0,
                0.0
            ]
        },
        {
            "units": "eV",
            "kpointConduction": [
                -7.19668434e-17,
                -0.944862979,
                -0.944862979
            ],
            "type": "indirect",
            "value": 0.65023092000000027,
            "kpointValence": [
                0.0,
                0.0,
                0.0
            ]
        }
    ],
    "name": "band_gaps"
}


class BasisTest(UnitTestBase):
    def setUp(self):
        super(BasisTest, self).setUp()

    def tearDown(self):
        super(BasisTest, self).setUp()

    def test_band_gaps(self):
        property_ = BandGaps("band_gaps", raw_data=BAND_GAPS_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_GAPS)
