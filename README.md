# ExPreSS

Exabyte Property Extractor, Sourcer, Serializer (ExPreSS) is a Python package to extract material- and simulation-related properties and serialize them according to the Exabyte data convention outlined in [Exabyte Source of Schemas and Examples (ESSE)](https://github.com/Exabyte-io/exabyte-esse). 

## Functionality

The package provides the below functionality:

- Extract material and workflow properties from Quantum ESPRESSO calculation and serialize them according to Exabyte data convention

- Extract material and workflow properties from VASP calculation and serialize them according to Exabyte data convention

- Parse the structure configs in string format (Poscar, PWScf input) and return material in JSON representation

- Parse data on disk and extract material and workflow properties and insert them into the database

## Architecture

The following diagram presents ExPreSS architecture. The package consists of two main components, properties and parsers.

![ExPreSS](https://user-images.githubusercontent.com/10528238/53059542-023a5380-346c-11e9-8f42-5ab018b4f293.png)

### Parsers

ExPreSS parsers are responsible for extracting raw data from available sources such as data on the disk and provide the data to properties classes. In order to make sure all parsers implement the same interfaces and abstract properties classes from the parsers implementations, a set a [Mixin](express/parsers/mixins) classes are provided which should be mixed with the parsers. The parsers must implement Mixins' abstract methods at the time of inheritance.

### Properties

ExPreSS properties classes are responsible to form the properties based on the raw data provided by the parsers and serialize the property according to Exabyte Data Convention outlined in [Exabyte Source of Schemas and Examples (ESSE)](https://github.com/Exabyte-io/exabyte-esse). 

## Installation

ExPreSS can be installed as a Python package either via PyPi or the repository as below.

#### PyPi

```bash
pip install express
```

#### Repository

0. Install [git-lfs](https://help.github.com/articles/installing-git-large-file-storage/) in order to pull the files stored on Git LFS.

1. Clone repository:
    
    ```bash
    git clone git@github.com:Exabyte-io/exabyte-express.git
    ```

2. Install [virtualenv](https://virtualenv.pypa.io/en/stable/) using [pip](https://pip.pypa.io/en/stable/) if not already present:

    ```bash
    pip install virtualenv
    ```

3. Create virtual environment and install required packages:

    ```bash
    cd exabyte-express
    virtualenv venv
    source venv/bin/activate
    export GIT_LFS_SKIP_SMUDGE=1
    pip install -e PATH_TO_EXPRESS_REPOSITORY
    ```

## Examples

The following example demonstrates how to initialize an ExPreSS class instance, to extract and serialize total energy produced in a Quantum ESPRESSO calculation.

```python

import json
from express import ExPrESS

kwargs = {
    "work_dir": "./tests/fixtures/espresso/test-001",
    "stdout_file": "./tests/fixtures/espresso/test-001/pw-scf.out"

}

express_ = ExPrESS("espresso", **kwargs)
print json.dumps(express_.property("total_energy"), indent=4)

```

In this example the final structure of a VASP calculation is extracted and is serialized to a material.

```python

import json
from express import ExPrESS

kwargs = {
    "work_dir": "./tests/fixtures/vasp/test-001",
    "stdout_file": "./tests/fixtures/vasp/test-001/vasp.out"

}

express_ = ExPrESS("vasp", **kwargs)
print json.dumps(express_.property("material", is_final_structure=True), indent=4)

```

One can use [StructureParser](express/parsers/structure.py) to extract materials from POSCAR or PW input files.

```python

import json
from express import ExPrESS

with open("./tests/fixtures/vasp/test-001/POSCAR") as f:
    poscar = f.read()

kwargs = {
    "structure_string": poscar,
    "structure_format": "poscar"
}

express_ = ExPrESS("structure", **kwargs)
print json.dumps(express_.property("material"), indent=4)

with open("./tests/fixtures/espresso/test-001/pw-scf.in") as f:
    pwscf_input = f.read()

kwargs = {
    "structure_string": pwscf_input,
    "structure_format": "espresso-in"
}

express_ = ExPrESS("structure", **kwargs)
print json.dumps(express_.property("material"), indent=4)

```

## Tests

There are two types of tests in ExPreSS, unit and integration, implemented in [Python Unit Testing Framework](https://docs.python.org/2/library/unittest.html).

### Unit Tests

Unit tests are used to assert properties are serialized according to Exabyte Data Convention. Properties classes are initialized with mocked parser data and then are serialized to assert functionality.

### Integration Tests

Parsers functionality is tested through integration tests. The parsers are initialized with the configuration specified in the [Tests Manifest](./tests/manifest.yaml) and then the functionality is asserted.

### Run Tests

Run the following command to run the tests.

```bash
sh run-tests.sh
```

## Contribution

We welcome feedback and contributions for other not-yet covered cases. We suggest forking this repository and introducing the adjustments there, the changes in the fork can further be considered for merging into this repository as explained in [GitHub Standard Fork and Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962).
