from tests.unit import UnitTestBase
from tests.unit.properties.raw_data import PHONON_DOS_RAW_DATA
from tests.unit.properties.non_scalar.two_dimensional_plot.phonon_dos import PHONON_DOS
from express.properties.non_scalar.two_dimensional_plot.phonon_dos import PhononDOS


class PhononDOSTest(UnitTestBase):
    def setUp(self):
        super(PhononDOSTest, self).setUp()

    def tearDown(self):
        super(PhononDOSTest, self).setUp()

    def test_phonon_dos(self):
        property_ = PhononDOS("phonon_dos", raw_data=PHONON_DOS_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PHONON_DOS)
