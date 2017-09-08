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
    },
    'volume': {
        'reference': 'express.properties.scalar.volume.Volume',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'density': {
        'reference': 'express.properties.scalar.density.Density',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'elemental_ratio': {
        'reference': 'express.properties.scalar.elemental_ratio.ElementalRatio',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'p-norm': {
        'reference': 'express.properties.scalar.p_norm.PNorm',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'zero_point_energy': {
        'reference': 'express.properties.scalar.zero_point_energy.ZeroPointEnergy',
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
            'express.parsers.mixins.reciprocal.ReciprocalDataMixin',
            'express.parsers.mixins.exabyteml.ExabyteMLDataMixin',
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
            'express.parsers.mixins.reciprocal.ReciprocalDataMixin',
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
    'material': {
        'reference': 'express.properties.material.Material',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'symmetry': {
        'reference': 'express.properties.non_scalar.symmetry.Symmetry',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'workflow:ml_predict': {
        'reference': 'express.properties.workflow.ExabyteMLPredictWorkflow',
        'mixins': [
            'express.parsers.mixins.exabyteml.ExabyteMLDataMixin',
        ]
    },
    'phonon_dos': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.phonon_dos.PhononDOS',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
    'phonon_dispersions': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.phonon_dispersions.PhononDispersions',
        'mixins': [
            'express.parsers.mixins.ionic.IonicDataMixin',
        ]
    },
}

CONVERGENCE_PROPERTIES = {
    'convergence_electronic': {
        'reference': 'express.properties.convergence.electronic.ConvergenceElectronic',
        'mixins': [
            'express.parsers.mixins.electronic.ElectronicDataMixin',
        ]
    },
    'convergence_ionic': {
        'reference': 'express.properties.convergence.ionic.ConvergenceIonic',
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
    'vasp': 'express.parsers.apps.vasp.parser.VaspParser',
    'pymatgen': 'express.parsers.pymatgen.PyMatGenParser',
    'exabyteml': 'express.parsers.exabyteml.ExabyteMLParser'
}
