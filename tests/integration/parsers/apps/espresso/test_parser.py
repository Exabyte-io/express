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

CONVERGENCE_ELECTRONIC = [
    1.40182131e+00,
    5.93994699e-01,
    7.00312479e-03,
    1.01988311e-03,
    4.20416063e-05,
    7.61919078e-06
]

STRESS_TENSOR = [
    [
        0.00050115,
        -1e-08,
        0.0
    ],
    [
        -1e-08,
        0.0005011,
        0.0
    ],
    [
        0.0,
        -0.0,
        0.00050111
    ]
]

ATOMIC_FORCES = [
    [
        -3.9e-07,
        -2.4e-07,
        0.0
    ],
    [
        3.9e-07,
        2.4e-07,
        0.0
    ]
]

TOTAL_ENERGY_CONTRIBUTION = {
    "harris_foulkes": {
        "name": "harris_foulkes",
        "value": -258.6293887585482
    },
    "ewald": {
        "name": "ewald",
        "value": -226.94126871332813
    },
    "one_electron": {
        "name": "one_electron",
        "value": 68.65366986552296
    },
    "hartree": {
        "name": "hartree",
        "value": 17.72349166363712
    },
    "exchange_correlation": {
        "name": "exchange_correlation",
        "value": -118.06528742483022
    },
    "smearing": {
        "name": "smearing",
        "value": -0.0
    }
}

CONVERGENCE_IONIC = [
    {
        "energy": -258.69395486970376
    },
    {
        "energy": -258.5950298816528
    },
    {
        "energy": -258.6270291223739
    },
    {
        "energy": -258.62924603477796
    },
    {
        "energy": -258.6293859013516
    },
    {
        "energy": -258.62939460899827
    }
]

IBZ_KPOINTS = [
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
    [-7.19668434e-17, -1.27477992e-16, -9.44862979e-01],
    [0.00000000e+00, -9.44862979e-01, 0.00000000e+00],
    [-7.19668434e-17, -9.44862979e-01, -9.44862979e-01],
    [-9.44862979e-01, 1.21698145e-16, 0.00000000e+00],
    [-9.44862979e-01, -9.44862979e-01, 0.00000000e+00]
]

EIGENVALUES_AT_KPOINTS_ZERO = {
    'kpoint': [0., 0., 0.],
    'weight': 0.25,
    'eigenvalues': [
        {
            'energies': [-5.5990059, 6.26931638, 6.26931998, 6.26934533,
                         8.71135349, 8.71135587, 8.71135838, 9.41550185],
            'spin': 0.5,
            'occupations': [1.0, 0.9999999999990231, 0.9999999999990226, 0.9999999999990189, 0.0, 0.0, 0.0, 0.0]
        }
    ]
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

    def test_espresso_nspins(self):
        self.assertEqual(self.parser.nspins(), 1)

    def test_espresso_eigenvalues_at_kpoints(self):
        self.assertDeepAlmostEqual(self.parser.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO, places=2)

    def test_espresso_ibz_k_points(self):
        self.assertDeepAlmostEqual(self.parser.ibz_k_points(), IBZ_KPOINTS, places=2)

    def test_espresso_dos(self):
        self.assertEqual(len(self.parser.dos()["energy"]), 453)

    def test_espresso_basis(self):
        self.assertDeepAlmostEqual(self.parser.basis(), BASIS, places=2)

    def test_espresso_lattice_vectors(self):
        self.assertDeepAlmostEqual(self.parser.lattice_vectors(), LATTICE, places=2)

    def test_espresso_convergence_electronic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_electronic(), CONVERGENCE_ELECTRONIC, places=2)

    def test_espresso_convergence_ionic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_ionic(), CONVERGENCE_IONIC, places=2)

    def test_espresso_stress_tensor(self):
        self.assertDeepAlmostEqual(self.parser.stress_tensor(), STRESS_TENSOR, places=2)

    def test_espresso_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), 73.72, places=2)

    def test_espresso_total_force(self):
        self.assertAlmostEqual(self.parser.total_force(), 1e-06, places=2)

    def test_espresso_atomic_forces(self):
        self.assertDeepAlmostEqual(self.parser.atomic_forces(), ATOMIC_FORCES, places=2)

    def test_espresso_total_energy_contributions(self):
        self.assertDeepAlmostEqual(self.parser.total_energy_contributions(), TOTAL_ENERGY_CONTRIBUTION, places=2)
