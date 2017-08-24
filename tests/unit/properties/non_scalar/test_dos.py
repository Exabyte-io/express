from tests.unit import UnitTestBase
from tests.unit.properties.non_scalar.dos import DOS
from tests.unit.properties.raw_data import DOS_RAW_DATA
from express.properties.non_scalar.two_dimensional_plot.density_of_states import DensityOfStates


class DensityOfStatesTest(UnitTestBase):
    def setUp(self):
        super(DensityOfStatesTest, self).setUp()

    def tearDown(self):
        super(DensityOfStatesTest, self).setUp()

    def test_dos(self):
        property_ = DensityOfStates("density_of_states", raw_data=DOS_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DOS)
