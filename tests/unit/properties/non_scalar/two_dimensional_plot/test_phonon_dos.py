from tests.unit import UnitTestBase
from tests.fixtures.data import PHONON_DOS_RAW_DATA
from express.properties.non_scalar.two_dimensional_plot.phonon_dos import PhononDOS

PHONON_DOS = {
    "yDataSeries": [[0.0, 1.7269000451847205e-08, 6.90749999421314e-08]],
    "xDataArray": [[-313.8999938964844, -312.8999938964844, -311.8999938964844]],
    "name": "phonon_dos",
    "xAxis": {"units": "cm-1", "label": "frequency"},
    "yAxis": {"units": "states/cm-1", "label": "Phonon DOS"},
}


class PhononDOSTest(UnitTestBase):
    def setUp(self):
        super(PhononDOSTest, self).setUp()

    def tearDown(self):
        super(PhononDOSTest, self).setUp()

    def test_phonon_dos(self):
        parser = self.get_mocked_parser("phonon_dos", PHONON_DOS_RAW_DATA)
        property_ = PhononDOS("phonon_dos", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PHONON_DOS)
