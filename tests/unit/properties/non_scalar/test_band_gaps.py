from tests.unit import UnitTestBase
from tests.data.raw_data import BAND_RAW_DATA
from express.properties.non_scalar.bandgaps import BandGaps

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
                -4.8471013318887174e-17,
                -0.4999999999999998,
                -0.5000000000000001
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


class BandGapsTest(UnitTestBase):
    def setUp(self):
        super(BandGapsTest, self).setUp()

    def tearDown(self):
        super(BandGapsTest, self).setUp()

    def test_band_gaps(self):
        property_ = BandGaps("band_gaps", raw_data=BAND_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_GAPS)
