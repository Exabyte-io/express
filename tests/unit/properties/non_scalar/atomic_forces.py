from tests.unit import UnitTestBase
from express.properties.non_scalar.atomic_forces import AtomicForces

ATOMIC_FORCES = {
    "units": "eV/bohr",
    "name": "atomic_forces",
    "values": [
        {
            "id": 1,
            "value": [
                -3.9e-07,
                -2.4e-07,
                0.0
            ]
        },
        {
            "id": 2,
            "value": [
                3.9e-07,
                2.4e-07,
                0.0
            ]
        }
    ]
}


class AtomicForcesTest(UnitTestBase):
    def setUp(self):
        super(AtomicForcesTest, self).setUp()

    def tearDown(self):
        super(AtomicForcesTest, self).setUp()

    def test_atomic_forces(self):
        raw_data = {
            "atomic_forces": [
                {
                    "id": 1,
                    "value": [
                        -3.9e-07,
                        -2.4e-07,
                        0.0
                    ]
                },
                {
                    "id": 2,
                    "value": [
                        3.9e-07,
                        2.4e-07,
                        0.0
                    ]
                }
            ]
        }
        property_ = AtomicForces("atomic_forces", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ATOMIC_FORCES)
