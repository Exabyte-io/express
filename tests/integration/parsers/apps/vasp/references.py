NSPIN = 1
PRESSURE = -93.51
TOTAL_FORCE = 1e-06
FERMI_ENERGY = 3.209
TOTAL_ENERGY = -8.208

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

CONVERGENCE_ELECTRONIC = [
    4.29350000e+02,
    -3.35170000e+02,
    -8.83550000e+01,
    -1.25260000e+01,
    -1.80150000e+00,
    1.94490000e-01,
    1.06520000e-01,
    -6.20760000e-03,
    -4.51130000e-04,
    -9.95120000e-05
]

STRESS_TENSOR = [
    [
        -93.50828664,
        -9.87e-06, 0.0
    ],
    [
        -9.87e-06,
        -93.50828335,
        0.0
    ],
    [
        -0.0,
        0.0,
        -93.50829984
    ]
]

ATOMIC_FORCES = [
    [
        0.0,
        -0.0,
        -0.0
    ],
    [
        -0.0,
        0.0,
        0.0
    ]
]

TOTAL_ENERGY_CONTRIBUTION = {
    "hartree": {
        "name": "hartree",
        "value": 856.53054951796355
    },
    "ewald": {
        "name": "ewald",
        "value": 1179.2331674536013
    },
    "exchange_correlation": {
        "name": "exchange_correlation",
        "value": 273.95823951955998
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
    [
        0,
        0,
        0,
    ],
    [
        0.5,
        0,
        0,
    ],
    [
        0.5,
        0.5,
        0,
    ]
]

EIGENVALUES_AT_KPOINTS_ZERO = {
    'kpoint': [
        0.0,
        0.0,
        0.0
    ],
    'weight': 0.125,
    'eigenvalues': [
        {
            'energies': [
                -130.6782,
                -130.6481,
                -86.7506,
                -86.7506,
                -86.7506,
                -86.7379,
                -86.7379,
                -86.7379,
                -9.0026,
                2.8751,
                2.8751,
                2.8752,
                5.2991,
                5.2991,
                5.2992,
                6.0054
            ]
            , 'spin': 0.5,
            'occupations': [
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                1.,
                0.,
                0.,
                0.,
                0.
            ]
        }

    ]
}
