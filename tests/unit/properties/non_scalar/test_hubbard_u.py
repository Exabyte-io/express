from tests.unit import UnitTestBase
from tests.fixtures.espresso.v7_2.references import HUBBARD_U_PARAMS
from express.properties.non_scalar.hubbard_u import HubbardU

HUBBARD_U_REFERENCE = {
    "name": "hubbard_u",
    "units": "eV",
    "values": HUBBARD_U_PARAMS["values"],
}


class HubbardUTest(UnitTestBase):
    def setUp(self):
        super(HubbardUTest, self).setUp()

    def tearDown(self):
        super(HubbardUTest, self).setUp()

    def test_hubbard_u(self):
        parser = self.get_mocked_parser("hubbard_u", HUBBARD_U_PARAMS)
        property_ = HubbardU("hubbard_u", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HUBBARD_U_REFERENCE)
