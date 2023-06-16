from tests.unit import UnitTestBase
from express.properties.scalar.density import Density

DENSITY = {"units": "g/cm^3", "name": "density", "value": 1}


class DensityTest(UnitTestBase):
    def setUp(self):
        super(DensityTest, self).setUp()

    def tearDown(self):
        super(DensityTest, self).setUp()

    def test_density(self):
        parser = self.get_mocked_parser("density", 1)
        property_ = Density("density", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DENSITY)
