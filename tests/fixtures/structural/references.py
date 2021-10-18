"""
Reference values for the molecule parser test calculations within ExPrESS
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
    "value": "Td",
    "tolerance": 0.3
}

CENTERED_BASIS_DATA = {
    "elements": [
        {
            "id": 1,
            "value": "C"
        },
        {
            "id": 2,
            "value": "H"
        },
        {
            "id": 3,
            "value": "H"
        },
        {
            "id": 4,
            "value": "H"
        },
        {
            "id": 5,
            "value": "H"
        }
    ],
    "name": "atomic_coordinates",
    "values": [
        {
            "id": 1,
            "value": [
                -0.00000,
                -0.00000,
                0.00000
            ]
        },
        {
            "id": 2,
            "value": [
                1.07000,
                -0.00000,
                0.00000
            ]
        },
        {
            "id": 3,
            "value": [
                -0.35666,
                0.79297,
                0.62361
            ]
        },
        {
            "id": 4,
            "value": [
                -0.35667,
                -0.93654,
                0.37493
            ]
        },
        {
            "id": 5,
            "value": [
                -0.35667,
                0.14358,
                -0.99854
            ]
        }
    ]
}

N_ATOMS_DATA = 5

"""
Reference values for the crystal parser test calculations within ExPrESS
"""

SPACE_GROUP_DATA = {
    "value": "C2/m",
    "tolerance": 0.3
}
