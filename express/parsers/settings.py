from math import pi
from bunch import Bunch


class Constant(object):
    """
    Constants from Konrad Hinsen's PhysicalQuantities module (1986 CODATA).
    """
    _c = 299792458.  # speed of light, m/s
    _mu0 = 4.e-7 * pi  # permeability of vacuum
    _eps0 = 1 / _mu0 / _c ** 2  # permittivity of vacuum
    _Grav = 6.67259e-11  # gravitational constant
    _hplanck = 6.6260755e-34  # Planck constant, J s
    _hbar = _hplanck / (2 * pi)  # Planck constant / 2pi, J s
    _e = 1.60217733e-19  # elementary charge
    _me = 9.1093897e-31  # electron mass
    _mp = 1.6726231e-27  # proton mass
    _Nav = 6.0221367e23  # Avogadro number
    _k = 1.380658e-23  # Boltzmann constant, J/K
    _amu = 1.6605402e-27  # atomic mass unit, kg
    BOHR = 4e10 * pi * _eps0 * _hbar ** 2 / _me / _e ** 2  # Bohr radius
    eV = 1.0
    HARTREE = _me * _e ** 3 / 16 / pi ** 2 / _eps0 ** 2 / _hbar ** 2
    RYDBERG = 0.5 * HARTREE
    Ry = RYDBERG
    Ha = HARTREE
    kJ = 1000.0 / _e
    kcal = 4.184 * kJ
    cm_inv_to_ev = 0.00012398  # cm^-1 to eV
    ry_bohr_to_eV_A = 25.71104309541616  # or RYDBERG / BOHR


GENERAL_REGEX = Bunch()
GENERAL_REGEX.update({
    'double_number': r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?',
    'int_number': r'[+-]?\d+'
})
