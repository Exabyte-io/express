from bunch import Bunch

PARSERS_REGISTRY = {
    'espresso': 'express.parsers.apps.espresso.parser.EspressoParser',
    'vasp': 'express.parsers.apps.vasp.parser.VaspParser'
}

GENERAL_REGEX = Bunch()
GENERAL_REGEX.update({
    'double_number': r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?',
    'int_number': r'[+-]?\d+'
})
