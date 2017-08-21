from tests.integration import IntegrationTestBase
from express.parsers.apps.espresso.parser import EspressoParser

BASIS = {
    "units": "angstrom",
    "elements": [
        {
            "id": 1,
            "value": "Si "
        },
        {
            "id": 2,
            "value": "Si "
        }
    ],
    "coordinates": [
        {
            "id": 1,
            "value": [
                0.0,
                0.0,
                0.0
            ]
        },
        {
            "id": 2,
            "value": [
                1.1159329259917776,
                0.789083666533198,
                1.9328525178272928
            ]
        }
    ]
}

LATTICE = {
    "units": "angstrom",
    "vectors": {
        "a": [
            3.3477985280590525,
            0.0,
            1.9328525178272928
        ],
        "c": [
            0.0,
            0.0,
            3.8657050356545857
        ],
        "b": [
            1.1159331759080586,
            3.1563346661327913,
            1.9328525178272928
        ],
        "alat": 1.0
    }
}


class TestEspressoParser(IntegrationTestBase):
    def setUp(self):
        super(TestEspressoParser, self).setUp()
        self.parser = EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoParser, self).setUp()

    def test_espresso_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), -19.008, places=2)

    def test_espresso_fermi_energy(self):
        self.assertAlmostEqual(self.parser.fermi_energy(), 6.607, places=2)

    def test_espresso_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), 73.72, places=2)

    def test_espresso_basis(self):
        self.assertDeepAlmostEqual(self.parser.basis(), BASIS, places=2)

    def test_espresso_lattice_vectors(self):
        self.assertDeepAlmostEqual(self.parser.lattice_vectors(), LATTICE, places=2)
