# ExPreSS

Exabyte Property Extractor, Sourcer, Serializer (ExPreSS) is a Python package to extract material- and simulation-related properties and serialize them according to the Exabyte data convention defined in [ESSE](https://github.com/Exabyte-io/exabyte-esse). 

## Functionality

- Extract material and workflow properties from Quantum Espresso calculation and serialize them according to Exabyte data convention

- Extract material and workflow properties from VASP calculation and serialize them according to Exabyte data convention

- Parse the structure configs in string format (Poscar, PWScf input) and return material in JSON representation

- Parse data on disk and extract material and workflow properties and insert them into the database

## Architecture

The following shows ExPreSS architecture.

![ExPreSS](https://user-images.githubusercontent.com/10528238/53045569-d0f95d80-3442-11e9-9cde-a005fb598c0c.png)

## Installation

ExPreSS can be install as a Python package either via PyPi or the repository as below.

#### PyPi

```bash
pip install express
```

#### Repository

```bash
virtualenv .venv
source .venv/bin/activate
export GIT_LFS_SKIP_SMUDGE=1
pip install -e PATH_TO_EXPRESS_REPOSITORY
```

## Parsers

## Properties

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

## Links
