from tests.unit import UnitTestBase
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

    def test_fermi_energy(self):
        property_ = ElementalRatio("elemental_ratio", raw_data={"elemental_ratios": {"Si": 0.6, "Ge": 0.4}}, element="Ge")
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ELEMENTAL_RATIO)
