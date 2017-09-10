import numpy as np

from tests.integration.parsers.apps.espresso.references import DOS

ATOMIC_FORCES_RAW_DATA = {
    "atomic_forces": [
        [
            -3.9e-07,
            -2.4e-07,
            0.0
        ], [
            3.9e-07,
            2.4e-07,
            0.0
        ]
    ]
}

BAND_RAW_DATA = {
    "eigenvalues_at_kpoints": [
        {
            "eigenvalues": [
                {
                    "energies": [
                        -5.5990059,
                        6.26931638,
                        6.26931998,
                        6.26934533,
                        8.71135349,
                        8.71135587,
                        8.71135838,
                        9.41550185
                    ],
                    "occupations": [
                        1.0,
                        0.9999999999990231,
                        0.9999999999990226,
                        0.9999999999990189,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                0,
                0,
                0
            ],
            "weight": 0.25
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        -3.30219959,
                        -0.66503974,
                        5.06084876,
                        5.0608702,
                        7.69496909,
                        9.49274379,
                        9.49275618,
                        13.89571002
                    ],
                    "occupations": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        2.191035831088034E-113,
                        0.0,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                0.28867514,
                0.20412412,
                -0.49999997
            ],
            "weight": 0.5
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        -3.30220019,
                        -0.6650363,
                        5.06084821,
                        5.06086954,
                        7.69496137,
                        9.49273868,
                        9.49275401,
                        13.89571914
                    ],
                    "occupations": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        2.199010455040857E-113,
                        0.0,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                0,
                -0.61237246,
                0
            ],
            "weight": 0.25
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        -1.51073812,
                        -1.51072293,
                        3.41069883,
                        3.41070722,
                        6.91957625,
                        6.91958498,
                        16.14829919,
                        16.1483028
                    ],
                    "occupations": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        4.579502952592552E-11,
                        4.573994582634171E-11,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                0.28867514,
                -0.40824834,
                -0.49999997
            ],
            "weight": 0.5
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        -3.30221054,
                        -0.66501391,
                        5.06085301,
                        5.06085524,
                        7.69495606,
                        9.49273487,
                        9.49273798,
                        13.89571883
                    ],
                    "occupations": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        2.204511701557367E-113,
                        0.0,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                -0.57735028,
                0.20412421,
                0
            ],
            "weight": 0.25
        },
        {
            "eigenvalues": [
                {
                    "energies": [
                        -1.51074222,
                        -1.5107195,
                        3.41069761,
                        3.41071003,
                        6.91957636,
                        6.91958424,
                        16.14830113,
                        16.14830247
                    ],
                    "occupations": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        4.579432877486831E-11,
                        4.574465149035778E-11,
                        0.0,
                        0.0
                    ],
                    "spin": 0.5
                }
            ],
            "kpoint": [
                -0.57735028,
                -0.40824824,
                0
            ],
            "weight": 0.25
        }
    ],
    "nspins": 1,
    "ibz_k_points": np.array([
        [
            0.0,
            0.0,
            0.0
        ],
        [
            -4.8471013318887174E-17,
            -4.8471013318887174E-17,
            -0.5000000000000001
        ],
        [
            0.0,
            -0.4999999999999998,
            0.0
        ],
        [
            -4.8471013318887174E-17,
            -0.4999999999999998,
            -0.5000000000000001
        ],
        [
            -0.4999999999999998,
            6.584042720160102E-17,
            0.0
        ],
        [
            -0.4999999999999998,
            -0.4999999999999998,
            0.0
        ]
    ]),
    "fermi_energy": 6.6,
    "band_gaps_direct": None,
    "band_gaps_indirect": None
}

BASIS_RAW_DATA = {
    "basis": {
        "elements": [
            {
                "id": 1,
                "value": "Si"
            },
            {
                "id": 2,
                "value": "Si"
            }
        ],
        "coordinates": {
            "values": [
                {
                    "id": 1,
                    "value": [
                        0,
                        0,
                        0
                    ]
                },
                {
                    "id": 2,
                    "value": [
                        0.25,
                        0.25,
                        0.25
                    ]
                }
            ]
        },
    }
}

LATTICE_RAW_DATA = {
    "lattice_vectors": {
        "vectors": {
            "a": [
                5.000000000,
                0.000121312,
                0.000131415
            ],
            "b": [
                0.000121312,
                5.000000000,
                0.000121314
            ],
            "c": [
                0.000121313,
                0.000121312,
                5.000000000
            ],
            "alat": 1.0,
        },

        "units": "angstrom"
    }

}

STRESS_TENSOR_RAW_DATA = {
    "stress_tensor": [
        [
            3,
            0,
            0
        ],
        [
            0,
            3,
            0
        ],
        [
            0,
            0,
            3
        ]
    ]
}

SYMMETRY_RAW_DATA = {
    "space_group_symbol": {
        "value": "Fd-3m",
        "tolerance": 0.3
    }
}

TOTAL_ENERGY_CONTRIBUTIONS_RAW_DATA = {
    "total_energy_contributions": {
        "ewald": {
            "name": "ewald",
            "value": 128376.45871064
        },
        "hartree": {
            "name": "hartree",
            "value": -145344.66902862
        },
        "exchangeCorrelation": {
            "name": "exchange_correlation",
            "value": 41.63693035
        }
    }
}

ELEMENTAL_RATIOS_RAW_DATA = {
    "elemental_ratios": {
        "Si": 0.6,
        "Ge": 0.4
    }
}

DOS_RAW_DATA = {
    "dos": DOS
}
