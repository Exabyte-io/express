from tests.unit import UnitTestBase
from tests.fixtures.data import ATOMIC_FORCES_RAW_DATA
from express.properties.non_scalar.atomic_forces import AtomicForces

ATOMIC_FORCES = {
    "units": "eV/angstrom",
    "name": "atomic_forces",
    "values": [{"id": 1, "value": [-3.9e-07, -2.4e-07, 0.0]}, {"id": 2, "value": [3.9e-07, 2.4e-07, 0.0]}],
}


class AtomicForcesTest(UnitTestBase):
    def setUp(self):
        super(AtomicForcesTest, self).setUp()

    def tearDown(self):
        super(AtomicForcesTest, self).setUp()

    def test_atomic_forces(self):
        parser = self.get_mocked_parser("atomic_forces", ATOMIC_FORCES_RAW_DATA)
        property_ = AtomicForces("atomic_forces", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ATOMIC_FORCES)
