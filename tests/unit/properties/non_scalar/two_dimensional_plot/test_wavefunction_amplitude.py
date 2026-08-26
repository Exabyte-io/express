from tests.unit import UnitTestBase
from express.properties.non_scalar.two_dimensional_plot.wavefunction_amplitude import WavefunctionAmplitude

RAW_DATA_ALAT = [
    [0.0, 0.0050251256, 0.0100502513, 0.0150753769, 0.0201005025],
    [0.0000322091, 0.0000072134, -0.0000218274, -0.0000540398, -0.0000883573]
]

ALAT_ANGSTROM = 10.0

CONVERTED_DATA_ANGSTROMS = [
    [x * ALAT_ANGSTROM for x in RAW_DATA_ALAT[0]],
    RAW_DATA_ALAT[1]
]

EXPECTED = {
    "name": "wavefunction_amplitude",
    "xDataArray": CONVERTED_DATA_ANGSTROMS[0],
    "yDataSeries": [CONVERTED_DATA_ANGSTROMS[1]],
    "xAxis": {"label": "coordinate", "units": "angstrom"},
    "yAxis": {"label": "amplitude"},
}


class WavefunctionAmplitudeTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_wavefunction_amplitude(self):
        parser = self.get_mocked_parser("wavefunction_amplitude", CONVERTED_DATA_ANGSTROMS)
        property_ = WavefunctionAmplitude("wavefunction_amplitude", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), EXPECTED)

