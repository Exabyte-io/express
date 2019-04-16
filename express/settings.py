ZERO_WEIGHT_KPOINT_THRESHOLD = 1e-7

SCALAR_PROPERTIES_MANIFEST = {
    'total_energy': {
        'reference': 'express.properties.scalar.total_energy.TotalEnergy'
    },
    'fermi_energy': {
        'reference': 'express.properties.scalar.fermi_energy.FermiEnergy'
    },
    'pressure': {
        'reference': 'express.properties.scalar.pressure.Pressure'
    },
    'total_force': {
        'reference': 'express.properties.scalar.total_force.TotalForce'
    },
    'volume': {
        'reference': 'express.properties.scalar.volume.Volume'
    },
    'density': {
        'reference': 'express.properties.scalar.density.Density'
    },
    'elemental_ratio': {
        'reference': 'express.properties.scalar.elemental_ratio.ElementalRatio'
    },
    'p-norm': {
        'reference': 'express.properties.scalar.p_norm.PNorm'
    },
    'zero_point_energy': {
        'reference': 'express.properties.scalar.zero_point_energy.ZeroPointEnergy'
    },
    'surface_energy': {
        'reference': 'express.properties.scalar.surface_energy.SurfaceEnergy'
    },
    'reaction_energy_barrier': {
        'reference': 'express.properties.scalar.reaction_energy_barrier.ReactionEnergyBarrier'
    },
}

NON_SCALAR_PROPERTIES_MANIFEST = {
    'band_gaps': {
        'reference': 'express.properties.non_scalar.bandgaps.BandGaps'
    },
    'density_of_states': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.density_of_states.DensityOfStates'
    },
    'band_structure': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.band_structure.BandStructure'
    },
    'stress_tensor': {
        'reference': 'express.properties.non_scalar.stress_tensor.StressTensor'
    },
    'atomic_forces': {
        'reference': 'express.properties.non_scalar.atomic_forces.AtomicForces'
    },
    'atomic_constraints': {
        'reference': 'express.properties.non_scalar.atomic_constraints.AtomicConstraints'
    },
    'total_energy_contributions': {
        'reference': 'express.properties.non_scalar.total_energy_contributions.TotalEnergyContributions'
    },
    'material': {
        'reference': 'express.properties.material.Material'
    },
    'symmetry': {
        'reference': 'express.properties.non_scalar.symmetry.Symmetry'
    },
    'workflow:ml_predict': {
        'reference': 'express.properties.workflow.ExabyteMLPredictWorkflow'
    },
    'phonon_dos': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.phonon_dos.PhononDOS'
    },
    'phonon_dispersions': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.phonon_dispersions.PhononDispersions'
    },
    'magnetic_moments': {
        'reference': 'express.properties.non_scalar.magnetic_moments.MagneticMoments'
    },
    'reaction_energy_profile': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.reaction_energy_profile.ReactionEnergyProfile'
    },
    'potential_profile': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.potential_profile.PotentialProfile'
    },
    'charge_density_profile': {
        'reference': 'express.properties.non_scalar.two_dimensional_plot.charge_density_profile.ChargeDensityProfile'
    },
}

CONVERGENCE_PROPERTIES = {
    'convergence_electronic': {
        'reference': 'express.properties.convergence.electronic.ConvergenceElectronic'
    },
    'convergence_ionic': {
        'reference': 'express.properties.convergence.ionic.ConvergenceIonic'
    }
}

PROPERTIES_MANIFEST = dict()
PROPERTIES_MANIFEST.update(CONVERGENCE_PROPERTIES)
PROPERTIES_MANIFEST.update(SCALAR_PROPERTIES_MANIFEST)
PROPERTIES_MANIFEST.update(NON_SCALAR_PROPERTIES_MANIFEST)

PARSERS_REGISTRY = {
    'espresso': 'express.parsers.apps.espresso.parser.EspressoParser',
    'vasp': 'express.parsers.apps.vasp.parser.VaspParser',
    'structure': 'express.parsers.structure.StructureParser',
    'exabyteml': 'express.parsers.exabyteml.ExabyteMLParser'
}

PRECISION = 4
