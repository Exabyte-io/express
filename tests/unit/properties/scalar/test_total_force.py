from tests.unit import UnitTestBase
from express.properties.scalar.total_force import TotalForce

TOTAL_FORCE = {
    "units": "eV/angstrom",
    "name": "total_force",
    "value": 1
}


class TotalForceTest(UnitTestBase):
    def setUp(self):
        super(TotalForceTest, self).setUp()

    def tearDown(self):
        super(TotalForceTest, self).setUp()

    def test_total_force(self):
        property_ = TotalForce("total_force", raw_data={"total_force": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), TOTAL_FORCE)
