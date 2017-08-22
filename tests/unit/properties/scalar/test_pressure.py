from tests.unit import UnitTestBase
from express.properties.scalar.pressure import Pressure

PRESSURE = {
    "units": "kbar",
    "name": "pressure",
    "value": 1
}


class PressureTest(UnitTestBase):
    def setUp(self):
        super(PressureTest, self).setUp()

    def tearDown(self):
        super(PressureTest, self).setUp()

    def test_pressure(self):
        property_ = Pressure("pressure", raw_data={"pressure": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PRESSURE)
