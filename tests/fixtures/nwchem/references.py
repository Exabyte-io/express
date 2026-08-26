"""
Reference values for the nwchem test calculations within ExPrESS
All nwchem output values are in hartrees. ExPrESS converts units to eV.
All reference energies are in eV.
"""

TOTAL_ENERGY = -2079.18666382721904

# Only the count and the edges of the spectrum are pinned; HOMO/LUMO below cover the frontier.
EIGENVALUES_AT_VECTORS_COUNT = 19
EIGENVALUES_AT_VECTORS_FIRST = {"vector": 1, "occupation": 2.0, "energy": -520.7096480731956}
EIGENVALUES_AT_VECTORS_LAST = {"vector": 19, "occupation": 0.0, "energy": 96.85556141135692}

# The *_INITIAL_GUESS values come from the initial-guess section preceding the SCF cycle; the tests
# assert the parser does not return them.
HOMO_ENERGY = -7.938587261191046
LUMO_ENERGY = 1.793148251055798
HOMO_ENERGY_INITIAL_GUESS = -12.800485418916242
LUMO_ENERGY_INITIAL_GUESS = 3.1242763921882197

# test-002/nwchem-frequency.log holds one orbital analysis section per optimization step.
EIGENVALUES_AT_VECTORS_MULTISTEP_COUNT = 18
EIGENVALUES_AT_VECTORS_MULTISTEP_FIRST = {"vector": 1, "occupation": 2.0, "energy": -520.5444749015667}
EIGENVALUES_AT_VECTORS_MULTISTEP_LAST = {"vector": 18, "occupation": 0.0, "energy": 70.15805296279406}

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

# test-001 declares `units au`, so these are its printed coordinates converted to angstrom. Read as
# angstrom instead they give an O-H of 1.81 A, which is what
# test_bond_length_of_an_atomic_units_block_is_physical guards against.
BASIS = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [0.0, 0.0, 0.11717600]},
        {"id": 1, "value": [0.0, 0.75695001, -0.46870401]},
        {"id": 2, "value": [0.0, -0.75695001, -0.46870401]},
    ],
}

# test-002 optimizes, so its first and last blocks differ.
# 6-31G* geometry: O-H 0.96866 A after relaxation, not the 6-31G 0.9758 A the Cypress feature pins.
INITIAL_BASIS_MULTISTEP = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [0.0, 0.0, 0.22143053]},
        {"id": 1, "value": [-1.43042811, 0.0, -0.88572214]},
        {"id": 2, "value": [1.43042811, 0.0, -0.88572214]},
    ],
}
FINAL_BASIS_MULTISTEP = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [0.0, 0.0, -0.11849741]},
        {"id": 1, "value": [-0.76261482, 0.0, -0.71575817]},
        {"id": 2, "value": [0.76261482, 0.0, -0.71575817]},
    ],
}

# What express serializes for test-002's final block: made's cubic padding sized to fit both
# structures, and the basis centered in it. Taken from a488316, where the parser did that itself --
# these are the numbers the move into the properties layer had to leave alone.
FINAL_CELL_EDGE_MULTISTEP = 5.721712
FINAL_CRYSTAL_COORDINATES_MULTISTEP = [
    [0.5, 0.5, 0.569589977],
    [0.366715633, 0.5, 0.465205011],
    [0.633284367, 0.5, 0.465205011],
]
