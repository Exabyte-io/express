#!/usr/bin/env bash
# File used to regenerate nwchem output files.

module add nwchem/702-g-485-ompi-110

mpirun --allow-run-as-root -np 1 nwchem.inp &> nwchem-total-energy.log
