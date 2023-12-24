from tests.unit import UnitTestBase
from tests.fixtures.espresso.v7_2.references import HUBBARD_V_NN_PARAMS
from express.properties.non_scalar.hubbard_v_nn import HubbardV_NN

HUBBARD_V_NN_REFERENCE = {
    "name": "hubbard_v_nn",
    "units": "eV",
    "values": HUBBARD_V_NN_PARAMS["values"],
}


class HubbardVNNTest(UnitTestBase):
    def setUp(self):
        super(HubbardVNNTest, self).setUp()

    def tearDown(self):
        super(HubbardVNNTest, self).setUp()

    def test_hubbard_v_nn(self):
        parser = self.get_mocked_parser("hubbard_v_nn", HUBBARD_V_NN_PARAMS)
        property_ = HubbardV_NN("hubbard_v_nn", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HUBBARD_V_NN_REFERENCE)
