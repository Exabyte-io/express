from unittest.mock import MagicMock

from tests.unit import UnitTestBase
from express.properties.non_scalar.bandgaps import BandGaps
from tests.fixtures.data import EIGENVALUES_AT_KPOINTS, IBZ_K_POINTS

BAND_GAPS = {
    "eigenvalues": [
        {
            "eigenvalues": [
                {"energies": [6.2693, 6.2693, 8.7114, 8.7114], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.25,
            "kpoint": [0, 0, 0],
        },
        {
            "eigenvalues": [
                {"energies": [5.0608, 5.0609, 7.695, 9.4927], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.5,
            "kpoint": [0.2887, 0.2041, -0.5],
        },
        {
            "eigenvalues": [
                {"energies": [5.0608, 5.0609, 7.695, 9.4927], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.25,
            "kpoint": [0.0, -0.6124, 0.0],
        },
        {
            "eigenvalues": [
                {"energies": [3.4107, 3.4107, 6.9196, 6.9196], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.5,
            "kpoint": [0.2887, -0.4082, -0.5],
        },
        {
            "eigenvalues": [
                {"energies": [5.0609, 5.0609, 7.695, 9.4927], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.25,
            "kpoint": [-0.5774, 0.2041, 0.0],
        },
        {
            "eigenvalues": [
                {"energies": [3.4107, 3.4107, 6.9196, 6.9196], "spin": 0.5, "occupations": [1.0, 1.0, 0.0, 0.0]}
            ],
            "weight": 0.25,
            "kpoint": [-0.5774, -0.4082, 0.0],
        },
    ],
    "values": [
        {
            "units": "eV",
            "kpointConduction": [0.0, 0.0, 0.0],
            "type": "direct",
            "spin": 0.5,
            "value": 2.4420081600000003,
            "kpointValence": [0.0, 0.0, 0.0],
            "eigenvalueValence": 6.26934533,
            "eigenvalueConduction": 8.71135349,
        },
        {
            "units": "eV",
            "kpointConduction": [-4.8471013318887174e-17, -0.4999999999999998, -0.5000000000000001],
            "type": "indirect",
            "spin": 0.5,
            "value": 0.65023092000000027,
            "kpointValence": [0.0, 0.0, 0.0],
            "eigenvalueValence": 6.26934533,
            "eigenvalueConduction": 6.91957625,
        },
    ],
    "name": "band_gaps",
}


class BandGapsTest(UnitTestBase):
    def setUp(self):
        super(BandGapsTest, self).setUp()

    def tearDown(self):
        super(BandGapsTest, self).setUp()

    def test_band_gaps(self):
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=1), "nspins")
        parser.attach_mock(MagicMock(return_value=6.6), "fermi_energy")
        parser.attach_mock(MagicMock(return_value=None), "band_gaps_direct")
        parser.attach_mock(MagicMock(return_value=None), "band_gaps_indirect")
        parser.attach_mock(MagicMock(return_value=IBZ_K_POINTS), "ibz_k_points")
        parser.attach_mock(MagicMock(return_value=EIGENVALUES_AT_KPOINTS), "eigenvalues_at_kpoints")
        property_ = BandGaps("band_gaps", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_GAPS)
