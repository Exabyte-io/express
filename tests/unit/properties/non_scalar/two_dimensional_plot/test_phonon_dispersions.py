from tests.unit import UnitTestBase
from express.properties.non_scalar.two_dimensional_plot.phonon_dispersions import PhononDispersions
from tests.unit.properties.non_scalar.two_dimensional_plot.phonon_dispersions import PHONON_DISPERSIONS, PHONON_DISPERSIONS_RAW_DATA


class PhononDispersionsTest(UnitTestBase):
    def setUp(self):
        super(PhononDispersionsTest, self).setUp()

    def tearDown(self):
        super(PhononDispersionsTest, self).setUp()

    def test_phonon_dispersions(self):
        property_ = PhononDispersions("phonon_dispersions", raw_data=PHONON_DISPERSIONS_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PHONON_DISPERSIONS)
