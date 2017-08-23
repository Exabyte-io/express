from tests.unit import UnitTestBase
from express.properties.scalar.density import Density

DENSITY = {
    "units": "g/cm^3",
    "name": "density",
    "value": 1
}


class DensityTest(UnitTestBase):
    def setUp(self):
        super(DensityTest, self).setUp()

    def tearDown(self):
        super(DensityTest, self).setUp()

    def test_density(self):
        property_ = Density("density", raw_data={"density": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DENSITY)
