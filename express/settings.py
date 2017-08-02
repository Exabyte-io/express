SCALAR_PROPERTIES_MANIFEST = {
    'total_energy': {
        'reference': 'express.properties.scalar.total_energy.TotalEnergy',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'fermi_energy': {
        'reference': 'express.properties.scalar.fermi_energy.FermiEnergy',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'pressure': {
        'reference': 'express.properties.scalar.pressure.Pressure',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'total_force': {
        'reference': 'express.properties.scalar.total_force.TotalForce',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    }
}

NON_SCALAR_PROPERTIES_MANIFEST = {
    'band_gaps': {
        'reference': 'express.properties.non_scalar.bandgaps.BandGaps',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
            'express.parsers.mixins.reciprocal.ReciprocalDataMixin'
        ]
    },
    'density_of_states': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.density_of_states.DensityOfStates',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'band_structure': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.band_structure.BandStructure',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
            'express.parsers.mixins.reciprocal.ReciprocalDataMixin'
        ]
    },
    'lattice': {
        'reference': 'express.properties.non_scalar.lattice.Lattice',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'basis': {
        'reference': 'express.properties.non_scalar.basis.Basis',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'stress_tensor': {
        'reference': 'express.properties.non_scalar.stress_tensor.StressTensor',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'atomic_forces': {
        'reference': 'express.properties.non_scalar.atomic_forces.AtomicForces',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'total_energy_contributions': {
        'reference': 'express.properties.non_scalar.total_energy_contributions.TotalEnergyContributions',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'space_group_symbol': {
        'reference': 'express.properties.non_scalar.space_group_symbol.SpaceGroupSymbol'
    }
}

CONVERGENCE_PROPERTIES = {
    'convergence_electronic': {
        'reference': 'express.properties.convergence.electronic.ConvergenceElectronic',
        'schema': 'science/models/dft/convergence/electronic.json',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'convergence_ionic': {
        'reference': 'express.properties.convergence.ionic.ConvergenceIonic',
        'schema': 'science/models/dft/convergence/ionic.json',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    }
}

PROPERTIES_MANIFEST = dict()
PROPERTIES_MANIFEST.update(CONVERGENCE_PROPERTIES)
PROPERTIES_MANIFEST.update(SCALAR_PROPERTIES_MANIFEST)
PROPERTIES_MANIFEST.update(NON_SCALAR_PROPERTIES_MANIFEST)

PARSERS_REGISTRY = {
    'espresso': 'express.parsers.apps.espresso.parser.EspressoParser',
    'vasp': 'express.parsers.apps.vasp.parser.VaspParser'
}
