"""
Reference values for the InChI test calculations within ExPrESS
"""
INCHI_DATA = {"inchi": "1S/CH4/h1H4", "inchi_key": "VNWKTOKETHGBQD-UHFFFAOYSA-N"}

# Reference data for Li CIF test (test-004) — verifies oxidation state stripping (Li0+ -> Li)
LI_CIF_BASIS = {
    "units": "crystal",
    "elements": [
        {"id": 0, "value": "Li"},
        {"id": 1, "value": "Li"},
        {"id": 2, "value": "Li"},
        {"id": 3, "value": "Li"},
        {"id": 4, "value": "Li"},
        {"id": 5, "value": "Li"},
        {"id": 6, "value": "Li"},
        {"id": 7, "value": "Li"},
        {"id": 8, "value": "Li"},
    ],
    "coordinates": [
        {"id": 0, "value": [0.666666670, 0.333333330, 0.110361250]},
        {"id": 1, "value": [0.000000000, 0.000000000, 0.222972080]},
        {"id": 2, "value": [0.000000000, 0.000000000, 0.000000000]},
        {"id": 3, "value": [0.333333330, 0.666666670, 0.443694590]},
        {"id": 4, "value": [0.666666670, 0.333333330, 0.556305410]},
        {"id": 5, "value": [0.666666670, 0.333333330, 0.333333330]},
        {"id": 6, "value": [0.000000000, 0.000000000, 0.777027920]},
        {"id": 7, "value": [0.333333330, 0.666666670, 0.889638750]},
        {"id": 8, "value": [0.333333330, 0.666666670, 0.666666670]},
    ],
}
