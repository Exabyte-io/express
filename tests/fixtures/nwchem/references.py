"""
Reference values for the nwchem test calculations within ExPrESS
All nwchem output values are in hartrees. ExPrESS converts units to eV.
All reference energies are in eV.
"""
TOTAL_ENERGY = -2079.18666382721904

TOTAL_ENERGY_CONTRIBUTION = {
    "one_electron": {"name": "one_electron", "value": -3350.531714067630674},
    "coulomb": {"name": "coulomb", "value": 1275.68347728573713},
    "exchange_correlation": {"name": "exchange_correlation", "value": -254.54658374762781},
    "nuclear_repulsion": {"name": "nuclear_repulsion", "value": 250.20815670232923},
}

BASIS = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [0.00000000, 0.00000000, 0.22143053]},
        {"id": 1, "value": [0.00000000, 1.43042809, -0.88572213]},
        {"id": 2, "value": [0.00000000, -1.43042809, -0.88572213]},
    ],
}
