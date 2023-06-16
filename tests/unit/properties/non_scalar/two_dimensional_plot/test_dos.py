from tests.unit import UnitTestBase
from tests.fixtures.data import DOS_RAW_DATA
from express.properties.non_scalar.two_dimensional_plot.density_of_states import DensityOfStates

DOS = {
    "legend": [
        {},
        {"electronicState": "2py", "element": "Si"},
        {"electronicState": "2px", "element": "Si"},
        {"electronicState": "1s", "element": "Si"},
        {"electronicState": "2pz", "element": "Si"},
    ],
    "name": "density_of_states",
    "xAxis": {"label": "energy", "units": "eV"},
    "xDataArray": [[-6.005000114440918, -5.954999923706055, -5.90500020980835]],
    "yAxis": {"label": "density of states", "units": "states/unitcell"},
    "yDataSeries": [
        [0.00012799999967683107, 0.0010100000072270632, 0.006130000110715628],
        [1.6499999980444308e-17, 1.3080000562020133e-16, 7.899999954541818e-16],
    ],
}


class DensityOfStatesTest(UnitTestBase):
    def setUp(self):
        super(DensityOfStatesTest, self).setUp()

    def tearDown(self):
        super(DensityOfStatesTest, self).setUp()

    def test_dos(self):
        parser = self.get_mocked_parser("dos", DOS_RAW_DATA)
        property_ = DensityOfStates("density_of_states", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DOS)
