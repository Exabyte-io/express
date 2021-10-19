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

N_ATOMS_DATA = 5

"""
Reference values for the crystal parser test calculations within ExPrESS
"""

SPACE_GROUP_DATA = {
    "value": "C2/m",
    "tolerance": 0.3
}
