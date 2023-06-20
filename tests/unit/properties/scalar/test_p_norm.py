from tests.unit import UnitTestBase
from express.properties.scalar.p_norm import PNorm
from tests.fixtures.data import ELEMENTAL_RATIOS_RAW_DATA

P_NORM = {"degree": 0, "name": "p-norm", "value": 2}


class PNormTest(UnitTestBase):
    def setUp(self):
        super(PNormTest, self).setUp()

    def tearDown(self):
        super(PNormTest, self).setUp()

    def test_p_norm(self):
        parser = self.get_mocked_parser("elemental_ratios", ELEMENTAL_RATIOS_RAW_DATA)
        property_ = PNorm("p-norm", parser, degree=0)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), P_NORM)
