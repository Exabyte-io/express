from tests.unit import UnitTestBase
from express.properties.scalar.pressure import Pressure

PRESSURE = {"units": "kbar", "name": "pressure", "value": 1}


class PressureTest(UnitTestBase):
    def setUp(self):
        super(PressureTest, self).setUp()

    def tearDown(self):
        super(PressureTest, self).setUp()

    def test_pressure(self):
        parser = self.get_mocked_parser("pressure", 1)
        property_ = Pressure("pressure", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), PRESSURE)
