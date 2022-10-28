from mock import MagicMock
import numpy as np
from tests.unit import UnitTestBase
from express.properties.non_scalar.averaged_potential import AveragedPotential


AVG_POTENTIAL = {
    "name": "averaged_electrostatic_potential",
    "macroscopicMinima": {
        "xDataArray": [3.15050167],
        "yDataSeries": [[-0.99996031]],
    }
}


class AveragedPotentialTest(UnitTestBase):
    def setUp(self):
        super(AveragedPotentialTest, self).setUp()

    def tearDown(self):
        super(AveragedPotentialTest, self).setUp()

    def create_mock_data(self):
        """
        Creates mock potential data based on cosine in the range [0, 2*pi].
        Exact minimum is at
          x   = pi
          m_x = -1
        """
        x = np.linspace(0, 6.28, 300)
        p_x = np.zeros(300)  # ignored for now
        m_x = np.cos(x)
        dtype = np.dtype([("x", float), ("p_x", float), ("m_x", float)])
        return np.array(list(zip(x, p_x, m_x)), dtype=dtype)

    def test_averaged_potential(self):
        averaged_potential_data = self.create_mock_data()
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=averaged_potential_data), "averaged_potential")
        property_ = AveragedPotential("averaged_electrostatic_potential", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), AVG_POTENTIAL)
