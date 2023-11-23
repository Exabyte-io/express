from tests.unit import UnitTestBase
from tests.fixtures.espresso.v7_2.references import HUBBARD_PARAMS
from express.properties.non_scalar.hubbard_parameters import HubbardParameters

HUBBARD_REFERENCE = {
    "name": "hubbard_parameters",
    "units": "eV",
    "category": HUBBARD_PARAMS["category"],
    "headers": HUBBARD_PARAMS["headers"],
    "values": HUBBARD_PARAMS["values"],
}


class HubbardParametersTest(UnitTestBase):
    def setUp(self):
        super(HubbardParametersTest, self).setUp()

    def tearDown(self):
        super(HubbardParametersTest, self).setUp()

    def test_hubbard_parameters(self):
        parser = self.get_mocked_parser("hubbard_parameters", HUBBARD_PARAMS)
        property_ = HubbardParameters("hubbard_parameters", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HUBBARD_REFERENCE)
