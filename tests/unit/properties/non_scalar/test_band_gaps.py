from tests.unit import UnitTestBase
from tests.data.raw_data import BAND_RAW_DATA
from express.properties.non_scalar.bandgaps import BandGaps

BAND_GAPS = {
    "eigenvalues": [
        {
            "eigenvalues": [
                {
                    "energies": [
                        6.26931998,
                        6.26934533,
                        8.71135349,
                        8.71135587
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                0,
                0,
                0
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        5.06084876,
                        5.0608702,
                        7.69496909,
                        9.49274379
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.5,
            "kpoint": [
                0.28867514,
                0.20412412,
                -0.49999997
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        5.06084821,
                        5.06086954,
                        7.69496137,
                        9.49273868
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                0.0,
                -0.61237246,
                0.0
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        3.41069883,
                        3.41070722,
                        6.91957625,
                        6.91958498
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.5,
            "kpoint": [
                0.28867514,
                -0.40824834,
                -0.49999997
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        5.06085301,
                        5.06085524,
                        7.69495606,
                        9.49273487
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                -0.57735028,
                0.20412421,
                0.0
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        3.41069761,
                        3.41071003,
                        6.91957636,
                        6.91958424
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        1.0,
                        0.0,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                -0.57735028,
                -0.40824824,
                0.0
            ]
        }
    ],
    "values": [
        {
            "units": "eV",
            "kpointConduction": [
                0.0,
                0.0,
                0.0
            ],
            "type": "direct",
            "value": 2.4420081600000003,
            "kpointValence": [
                0.0,
                0.0,
                0.0
            ]
        },
        {
            "units": "eV",
            "kpointConduction": [
                -4.8471013318887174e-17,
                -0.4999999999999998,
                -0.5000000000000001
            ],
            "type": "indirect",
            "value": 0.65023092000000027,
            "kpointValence": [
                0.0,
                0.0,
                0.0
            ]
        }
    ],
    "name": "band_gaps"
}


class BandGapsTest(UnitTestBase):
    def setUp(self):
        super(BandGapsTest, self).setUp()

    def tearDown(self):
        super(BandGapsTest, self).setUp()

    def test_band_gaps(self):
        property_ = BandGaps("band_gaps", raw_data=BAND_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_GAPS)
