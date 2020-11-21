#!/usr/bin/env bash

module add /applications/nwchem/66-i-174-impi-044

mpirun --allow-run-as-root -np 1 nwchem.inp &> nwchem.log
