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

# test-001 is a single point, so its initial and final structures are the same one printed block.
# Its input declares `units au`, so the coordinates below are the printed ones converted to
# angstrom; they are then centered in the cell that made's convention derives for a molecule.
BASIS = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [1.51390003, 1.51390003, 1.90448670]},
        {"id": 1, "value": [1.51390003, 2.27085004, 1.31860669]},
        {"id": 2, "value": [1.51390003, 0.75695001, 1.31860669]},
    ],
}
LATTICE_VECTORS = {
    "vectors": {"a": [3.02780005, 0.0, 0.0], "b": [0.0, 3.02780005, 0.0], "c": [0.0, 0.0, 3.02780005], "alat": 1}
}

# test-002 optimizes, so its first and last blocks differ — and so do the cells derived from them.
# 6-31G* geometry: O-H 0.96866 A after relaxation, not the 6-31G 0.9758 A the Cypress feature pins.
INITIAL_BASIS_MULTISTEP = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [2.86085618, 2.86085618, 3.59895795]},
        {"id": 1, "value": [1.43042809, 2.86085618, 2.49180529]},
        {"id": 2, "value": [4.29128427, 2.86085618, 2.49180529]},
    ],
}
FINAL_BASIS_MULTISTEP = {
    "units": "angstrom",
    "elements": [{"id": 0, "value": "O"}, {"id": 1, "value": "H"}, {"id": 2, "value": "H"}],
    "coordinates": [
        {"id": 0, "value": [2.86085618, 2.86085618, 3.25903001]},
        {"id": 1, "value": [2.09824137, 2.86085618, 2.66176926]},
        {"id": 2, "value": [3.62347099, 2.86085618, 2.66176926]},
    ],
}
# One cell for both structures: an optimization moves atoms inside a fixed box, it does not resize
# the box. Deriving a second, tighter cell from the relaxed coordinates would shrink-wrap the
# molecule and leave initial and final incomparable.
LATTICE_VECTORS_MULTISTEP = {
    "vectors": {"a": [5.72171236, 0.0, 0.0], "b": [0.0, 5.72171236, 0.0], "c": [0.0, 0.0, 5.72171236], "alat": 1}
}
