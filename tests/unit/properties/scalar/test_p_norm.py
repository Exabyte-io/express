from tests.unit import UnitTestBase
from express.properties.scalar.p_norm import PNorm

P_NORM = {
    "degree": 0,
    "name": "p-norm",
    "value": 2
}


class PNormTest(UnitTestBase):
    def setUp(self):
        super(PNormTest, self).setUp()

    def tearDown(self):
        super(PNormTest, self).setUp()

    def test_p_norm(self):
        property_ = PNorm("p-norm", raw_data={"elemental_ratios": {"Si": 0.6, "Ge": 0.4}}, degree=0)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), P_NORM)
