from tests.unit import UnitTestBase
from tests.data.raw_data import ELEMENTAL_RATIOS_RAW_DATA
from express.properties.scalar.elemental_ratio import ElementalRatio

ELEMENTAL_RATIO = {
    "name": "elemental_ratio",
    "value": 0.4,
    "element": "Ge"
}


class ElementalRatioTest(UnitTestBase):
    def setUp(self):
        super(ElementalRatioTest, self).setUp()

    def tearDown(self):
        super(ElementalRatioTest, self).setUp()

    def test_elemental_ratio(self):
        property_ = ElementalRatio("elemental_ratio", raw_data=ELEMENTAL_RATIOS_RAW_DATA, element="Ge")
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ELEMENTAL_RATIO)
