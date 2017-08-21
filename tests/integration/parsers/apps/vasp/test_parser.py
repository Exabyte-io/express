from tests.integration import IntegrationTestBase
from express.parsers.apps.vasp.parser import VaspParser

BASIS = {
    "units": "angstrom",
    "elements": [
        {
            "id": 0,
            "value": "Si"
        },
        {
            "id": 1,
            "value": "Si"
        }
    ],
    "coordinates": [
        {
            "id": 0,
            "value": [
                0.0,
                0.0,
                0.0
            ]
        },
        {
            "id": 1,
            "value": [
                1.1163067500000001,
                0.789348,
                1.9335
            ]
        }
    ]
}

LATTICE = {
    "vectors": {
        "a": [
            3.34892,
            0.0,
            1.9335
        ],
        "units": "angstrom",
        "c": [
            0.0,
            0.0,
            3.867
        ],
        "b": [
            1.116307,
            3.157392,
            1.9335
        ],
        "alat": 1.0
    }
}


class TestVaspParser(IntegrationTestBase):
    def setUp(self):
        super(TestVaspParser, self).setUp()
        self.parser = VaspParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestVaspParser, self).setUp()

    def test_vasp_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), -8.208, places=2)

    def test_vasp_fermi_energy(self):
        self.assertAlmostEqual(self.parser.fermi_energy(), 3.209, places=2)

    def test_vasp_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), -93.51, places=2)

    def test_vasp_basis(self):
        self.assertDeepAlmostEqual(self.parser.basis(), BASIS, places=2)

    def test_vasp_lattice_vectors(self):
        self.assertDeepAlmostEqual(self.parser.lattice_vectors(), LATTICE, places=2)
