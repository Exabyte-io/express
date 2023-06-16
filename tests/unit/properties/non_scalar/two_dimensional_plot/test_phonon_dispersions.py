from tests.unit import UnitTestBase
from tests.fixtures.data import PHONON_DISPERSIONS_RAW_DATA
from express.properties.non_scalar.two_dimensional_plot.phonon_dispersions import PhononDispersions

PHONON_DISPERSIONS = {
    "yDataSeries": [[-6e-06, -6.859784], [-6e-06, -6.859784]],
    "xDataArray": [[0.0, 0.0, 0.0], [0.0, 0.05, 0.05]],
    "name": "phonon_dispersions",
    "xAxis": {"units": "crystal", "label": "qpoints"},
    "yAxis": {"units": "cm-1", "label": "frequency"},
}


class PhononDispersionsTest(UnitTestBase):
    def setUp(self):
        super(PhononDispersionsTest, self).setUp()

    def tearDown(self):
        super(PhononDispersionsTest, self).setUp()

    def test_phonon_dispersions(self):
        parser = self.get_mocked_parser("phonon_dispersions", PHONON_DISPERSIONS_RAW_DATA)
        property_ = PhononDispersions("phonon_dispersions", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PHONON_DISPERSIONS)
