from tests.unit import UnitTestBase
from tests.data.raw_data import BAND_RAW_DATA, BAND_STRUCTURE, HSE_BAND_RAW_DATA, HSE_BAND_STRUCTURE
from express.properties.non_scalar.two_dimensional_plot.band_structure import BandStructure


class BandStructureTest(UnitTestBase):
    def setUp(self):
        super(BandStructureTest, self).setUp()

    def tearDown(self):
        super(BandStructureTest, self).setUp()

    def test_band_structure(self):
        property_ = BandStructure("band_structure", raw_data=BAND_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_STRUCTURE)

    def test_hse_band_structure(self):
        property_ = BandStructure("band_structure", raw_data=HSE_BAND_RAW_DATA, remove_non_zero_weight_kpoints=True)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HSE_BAND_STRUCTURE)
