"""
Reference values for the nwchem test calculations within ExPrESS
All nwchem output values are in hartrees. ExPrESS converts units to eV.
All reference energies are in eV.
"""
TOTAL_ENERGY = -2079.18666382721904
# HOMO/LUMO from the final orbital analysis section. The *_INITIAL_GUESS values come from the
# initial-guess section and are used by the tests to check the parser does not return them.
HOMO_ENERGY = -7.938587261191046
LUMO_ENERGY = 1.793148251055798
HOMO_ENERGY_INITIAL_GUESS = -12.800485418916242
LUMO_ENERGY_INITIAL_GUESS = 3.1242763921882197

# From test-002/nwchem-frequency.log, whose output contains several orbital analysis sections
# (one per geometry-optimization step); the parser must read the last one.
HOMO_ENERGY_MULTISTEP = -7.8966272890902385
LUMO_ENERGY_MULTISTEP = 1.7759215328081597
HOMO_ENERGY_MULTISTEP_INITIAL_GUESS = -10.187320671325603
LUMO_ENERGY_MULTISTEP_INITIAL_GUESS = -3.5424611206222094

ZERO_POINT_ENERGY = 0.5748347036575007
THERMAL_CORRECTION_TO_ENERGY = 15.033
THERMAL_CORRECTION_TO_ENTHALPY = 15.626

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
