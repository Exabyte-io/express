from unittest.mock import MagicMock

from tests.unit import UnitTestBase
from express.properties.non_scalar.two_dimensional_plot.band_structure import BandStructure
from tests.fixtures.data import BAND_STRUCTURE, HSE_EIGENVALUES_AT_KPOINTS, HSE_BAND_STRUCTURE, EIGENVALUES_AT_KPOINTS


class BandStructureTest(UnitTestBase):
    def setUp(self):
        super(BandStructureTest, self).setUp()

    def tearDown(self):
        super(BandStructureTest, self).setUp()

    def test_band_structure(self):
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=1), "nspins")
        parser.attach_mock(MagicMock(return_value=EIGENVALUES_AT_KPOINTS), "eigenvalues_at_kpoints")
        property_ = BandStructure("band_structure", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_STRUCTURE)

    def test_hse_band_structure(self):
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=1), "nspins")
        parser.attach_mock(MagicMock(return_value=HSE_EIGENVALUES_AT_KPOINTS), "eigenvalues_at_kpoints")
        property_ = BandStructure("band_structure", parser, remove_non_zero_weight_kpoints=True)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HSE_BAND_STRUCTURE)
