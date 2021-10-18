"""
Reference values for the InChI test calculations within ExPrESS
"""
INCHI_DATA = {
    "inchi": "1S/CH4/h1H4",
    "inchi_key": "VNWKTOKETHGBQD-UHFFFAOYSA-N"
}

MAX_RADII_DATA = {
    "name": "molecule-max-radii",
    "atom-pair": [
        {
            "id": 1
        },
        {
            "id": 4
        }
    ],
    "distance": {
        "value": 1.7473070445926022,
        "units": "angstrom"
    }
}

POINT_GROUP_DATA = {
    "name": "symmetry",
    "pointGroupSymbol": "Td",
    "tolerance": {
        "units": "angstrom",
        "value": 0.3
    }
}

CENTERED_BASIS_DATA = [
    [
        'C',
        -0.00000,
        -0.00000,
        0.00000
    ],
    [
        'H',
        1.07000,
        -0.00000,
        0.00000
    ],
    [
        'H',
        -0.35666,
        0.79297,
        0.62361
    ],
    [
        'H',
        -0.35667,
        -0.93654,
        0.37493
    ],
    [
        'H',
        -0.35667,
        0.14358,
        -0.99854
    ]
]

N_ATOMS_DATA = 5
