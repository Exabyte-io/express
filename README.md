# ExPreSS

Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.

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
