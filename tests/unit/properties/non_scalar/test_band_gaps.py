from tests.unit import UnitTestBase
from tests.data.raw_data import BAND_RAW_DATA
from express.properties.non_scalar.bandgaps import BandGaps

BAND_GAPS = {
    "eigenvalues": [
        {
            "eigenvalues": [
                {
                    "energies": [
                        -5.5990059,
                        6.26931638,
                        6.26931998,
                        6.26934533,
                        8.71135349
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        0.9999999999990231,
                        0.9999999999990226,
                        0.9999999999990189,
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
                        5.0608702,
                        7.69496909,
                        9.49274379
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        2.191035831088034e-113,
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
                        5.06086954,
                        7.69496137,
                        9.49273868
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        2.199010455040857e-113,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                0,
                -0.61237246,
                0
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        3.41070722,
                        6.91957625,
                        6.91958498,
                        16.14829919
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        4.579502952592552e-11,
                        4.573994582634171e-11,
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
                        5.06085524,
                        7.69495606,
                        9.49273487
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        2.204511701557367e-113,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                -0.57735028,
                0.20412421,
                0
            ]
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        3.41071003,
                        6.91957636,
                        6.91958424,
                        16.14830113
                    ],
                    "spin": 0.5,
                    "occupations": [
                        1.0,
                        4.579432877486831e-11,
                        4.574465149035778e-11,
                        0.0
                    ]
                }
            ],
            "weight": 0.25,
            "kpoint": [
                -0.57735028,
                -0.40824824,
                0
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
