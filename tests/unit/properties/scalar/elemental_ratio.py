from tests.unit import UnitTestBase
from tests.fixtures.data import ELEMENTAL_RATIOS_RAW_DATA
from express.properties.scalar.elemental_ratio import ElementalRatio

ELEMENTAL_RATIO = {"name": "elemental_ratio", "value": 0.4, "element": "Ge"}


class ElementalRatioTest(UnitTestBase):
    def setUp(self):
        super(ElementalRatioTest, self).setUp()

    def tearDown(self):
        super(ElementalRatioTest, self).setUp()

    def test_elemental_ratio(self):
        parser = self.get_mocked_parser("elemental_ratios", ELEMENTAL_RATIOS_RAW_DATA)
        property_ = ElementalRatio("elemental_ratio", parser, element="Ge")
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ELEMENTAL_RATIO)
