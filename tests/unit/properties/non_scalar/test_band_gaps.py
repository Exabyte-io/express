from tests.unit import UnitTestBase
from express.properties.non_scalar.bandgaps import BandGaps

BAND_GAPS = {
    "name": "band_gaps",
    "values": [
        {
            "type": "direct",
            "kpointConduction": [
                0,
                0,
                0
            ],
            "kpointValence": [
                0,
                0,
                0
            ],
            "value": 0.0947,
            "units": "rydberg"
        },
        {
            "type": "indirect",
            "value": 0.00,
            "units": "rydberg"
        }
    ]
}


class BandGapsTest(UnitTestBase):
    def setUp(self):
        super(BandGapsTest, self).setUp()

    def tearDown(self):
        super(BandGapsTest, self).setUp()

    def test_band_gaps(self):
        raw_data = {
            "nspins": "",
            "ibz_k_points": "",
            "fermi_energy": "",
            "eigenvalues_at_kpoints": ""
        }
        property_ = BandGaps("band_gaps", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_GAPS)
