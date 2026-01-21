from tests.unit import UnitTestBase
from express.properties.non_scalar.two_dimensional_plot.wavefunction_amplitude import WavefunctionAmplitude


WAVEFUNCTION_AMPLITUDE_RAW_DATA = [
    [0.0, 0.0050251256, 0.0100502513, 0.0150753769, 0.0201005025],
    [0.0000322091, 0.0000072134, -0.0000218274, -0.0000540398, -0.0000883573]
]

WAVEFUNCTION_AMPLITUDE = {
    "name": "wavefunction_amplitude",
    "xDataArray": [0.0, 0.0050251256, 0.0100502513, 0.0150753769, 0.0201005025],
    "yDataSeries": [[0.0000322091, 0.0000072134, -0.0000218274, -0.0000540398, -0.0000883573]],
    "xAxis": {"label": "coordinate", "units": "angstrom"},
    "yAxis": {"label": "amplitude", "units": "a.u."},
}


class WavefunctionAmplitudeTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_wavefunction_amplitude(self):
        parser = self.get_mocked_parser("wavefunction_amplitude", WAVEFUNCTION_AMPLITUDE_RAW_DATA)
        property_ = WavefunctionAmplitude("wavefunction_amplitude", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), WAVEFUNCTION_AMPLITUDE)

