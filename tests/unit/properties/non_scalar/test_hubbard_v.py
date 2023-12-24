from tests.unit import UnitTestBase
from tests.fixtures.espresso.v7_2.references import HUBBARD_V_PARAMS
from express.properties.non_scalar.hubbard_v import HubbardV

HUBBARD_V_REFERENCE = {
    "name": "hubbard_v",
    "units": "eV",
    "values": HUBBARD_V_PARAMS["values"],
}


class HubbardVTest(UnitTestBase):
    def setUp(self):
        super(HubbardVTest, self).setUp()

    def tearDown(self):
        super(HubbardVTest, self).setUp()

    def test_hubbard_v(self):
        parser = self.get_mocked_parser("hubbard_v", HUBBARD_V_PARAMS)
        property_ = HubbardV("hubbard_v", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HUBBARD_V_REFERENCE)
